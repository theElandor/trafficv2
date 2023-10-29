# Vehicles coordination algorithms
from audioop import cross
from datetime import datetime
import multiprocessing
import math
import numpy as np
from OrderedEdges import OrderedEdges
from LinkedList import ListNode
import os

from src.utility_print import *
from src.cooperative import Cooperative
from src.competitive import Competitive
from src.utils import *
from src.listeners import *
from src.CrossGraph import Graph

"""
main program that handles the results of the simulation.
The data containing waiting times (crossroad_total, crossroad_vehicles, traffic_total, traffic_vehicles, ecc..)
will be stored in the data/ folder.
If the simulation contains (for example) 140 vehicles, the data will also be written in qlearn_data/140/ folder.
It is usefull to store the data according to the number of vehicles for evaluation plots.
"""

def initialize_files():
    """
    Function needed to initialize text files(csv format)
    used for plotting
    """
    with open("bids.txt", "w") as bid:
        bid.write("crossroad,amount\n")
    with open("flow.txt", "w") as flow:
        flow.write("crossroad,veics\n")
    with open("encounters.txt", "w") as en:
        en.write("crossroad,trafficStopList\n")
    with open("reward.txt", "w") as en:
        pass
    with open("actions.txt", "w") as ac:
        pass
    with open("Q-values.txt", "w") as qv:
        pass

def testSaveDir(settings):
    """
    Function that checks if the folders where the output will be written exist.
    """
    veics = str(settings['VS'])
    model_version = settings['MV']
    simulation_index = str(settings['AI'])
    path = "qlearn_data/"+str(veics)+"/"
    compared_path = "models/{}/compared_exp/average_{}T/".format(model_version, veics)
    final_path = "models/{}/compared_exp/average_{}T/{}".format(model_version, veics, simulation_index)
    # reminder prints
    print(path)
    print(compared_path)
    print(final_path)
    # create paths
    paths = [path, compared_path, final_path]
    for p in paths:
        if not os.path.exists(p):
            c = input("{} destination folder does not exist. Do you want to create it now? (y/n)".format(p))
            if c == "y":
                os.mkdir(p)
            else:
                return False
    return True

def run(settings, model_chosen, chunk_name=0, time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), sumoBinary="/usr/bin/sumo", extra_configs=None):
    sumoCmd = [sumoBinary, "-c", "sumo_cfg/project.sumocfg", "--threads", "8"]

    """
        Simulation runs
    """
    try:
        traci.start(sumoCmd)
        crossroads_names = retrieveCrossroadsNames()
        crossroads, edges, in_edges = infrastructureRetrieving(crossroads_names)

        oe = OrderedEdges()
        in_edges = oe.getInEdges()
        out_edges = getOutEdges(in_edges)
        routes = traci.route.getIDList()
        print(routes)
        spawnCars(settings, routes)
        if model_chosen == 'Coop' or model_chosen == 'Comp':
            listener = Listener(settings['Stp'], settings, routes, crossroads_names)
        else:
            listener = AutonomousListener(settings['Stp'], settings)
        traci.addStepListener(listener)

        log_file_initialization(chunk_name, settings, model_chosen, listener, time)
        # log_print("Simulation starts")
        if model_chosen == 'Coop':
            model = Cooperative(settings, extra_configs)
        elif model_chosen == 'Comp':
            model = Competitive(settings)
        # NOTE: EB and DA don't need a dedicated class, the specific vehicles 'are' the classes        
        while True:
            if model_chosen == 'EB' or model_chosen == 'DA':
                traci.simulationStep()
            else:
                dc = {}
                idle_times = {}
                traffic = {}
                for crossroad in crossroads.keys(): #for each crossroad
                    # log_print('Handling crossroad {}'.format(crossroad))
                    dc[crossroad], idle_times[crossroad], traffic[crossroad]= model.intersectionControl(crossroads[crossroad])
                    # after this function, dc[crossroad] contains ordered list of cars that have to depart from crossing
                    if not listener.getSimulationStatus():
                        break
                departCars(settings, dc, idle_times, listener, in_edges, out_edges, extra_configs,traffic)
                traci.simulationStep()
            if not listener.getSimulationStatus():
                print("Simulation finished!")
                traci.close()
                break
        model.bidder.save()
        
        # if the bidder is active, then write on file
        # the amount of money saved and the total number
        # of reroutes. This way we can compute the
        # average amount of money saved on each route.
        
        if model.test_veic != "?":
            with open("qlearn_data/"+str(settings['VS'])+"/gained_"+str(model.simulationName)+".txt", "w") as t:
                t.write(str(model.trained_veic.gained_money)+"\n")
                t.write(str(model.trained_veic.total_reroutes)+"\n")
            if str(model.simulationName) != "random":
                with open("models/{}/compared_exp/average_{}T/{}/gained_{}.txt".format(settings['MV'], str(settings['VS']), str(settings['AI']), str(model.simulationName)), "w") as f:
                    f.write(str(model.trained_veic.gained_money)+"\n")
                    f.write(str(model.trained_veic.total_reroutes)+"\n")
                    
    except traci.exceptions.FatalTraCIError:
        print("Saving manager brain....")
        print("Simulation interrupted")
    return crossroads_names, model

# runs the simulation with the RUN function, then just plots the data.
def sim(configs, chunk_name=0, time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), sumoBinary="/usr/bin/sumo-gui", lock=None, q=None, extra_configs=None):
    excluded_settings = ['model', 'CP', 'MCA', 'E', 'Bdn', 'Rts', 'RUNS']
    # change qlearn variable to write different file in directory
    crossroads_names, model = run(configs, configs['model'], chunk_name, time, sumoBinary, extra_configs)
    cross_total, traffic_total, df_waiting_times, crossroads_wt, traffic_wt, crossroad_vehicles, traffic_vehicles = collectWT(crossroads_names)
    simulationName = model.simulationName
    file_name = f'{chunk_name}[' + time + ']' + configs['model']
    for s in configs.keys():
        if s not in excluded_settings:
            file_name += '_' + s + ':' + str(settings[s])

    with open('data/'+file_name+'|extra_configs.txt', "w") as f:
        for k in extra_configs:
            f.write(k + ":")
            f.write(str(extra_configs[k]))
            f.write(' ')
    file_name += '|{}'

    data_file = 'data/' + file_name
    df_waiting_times.to_csv(data_file.format('global') + '.txt', index_label=False, index=False)
    cross_total.to_csv(data_file.format('cross-total') + '.txt', index_label=False)
    traffic_total.to_csv(data_file.format('traffic-total') + '.txt', index_label=False)
    crossroads_wt.to_csv(data_file.format('crossroads') + '.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    traffic_wt.to_csv(data_file.format('traffic') + '.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    
    crossroad_vehicles.to_csv('./qlearn_data/'+str(configs['VS'])+'/crossroad_'+str(simulationName)+'.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    traffic_vehicles.to_csv('./qlearn_data/'+str(configs['VS'])+'/traffic_'+str(simulationName)+'.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

    crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], str(configs['VS']), str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    traffic_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/traffic_{}.txt".format(configs['MV'], str(configs['VS']), str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])    

    crossroad_vehicles.to_csv(data_file.format('crossroad-vehicles') + '.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    traffic_vehicles.to_csv(data_file.format('traffic-vehicles') + '.txt', header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    
    print(OKGREEN + f'Raw data written in data/{chunk_name}[{time}]{configs["model"]}|*.txt' + ENDC)

    if chunk_name == 0:
        # NOTE: there is a problem for subsequent processes trying to plot theirs results, they quit from 'sim' and don't put results in queue
        # Plots are of the first run
        plot(crossroads_wt, 'Crossroads', 'Average crossroad waiting time for each crossroad', file_name.format('crossroads') + '.png')
        plot(traffic_wt, 'Crossroads', 'Average traffic waiting time for each crossroad', file_name.format('traffic') + '.png')
        plot(crossroad_vehicles, 'Cars', 'Average crossroad waiting time of each car', file_name.format('crossroad-vehicles') + '.png')
        plot(traffic_vehicles, 'Cars', 'Average traffic waiting time of each car', file_name.format('traffic-vehicles') + '.png')

    '''
    cross_total['mean'] = 0 if math.isnan(cross_total['mean']) else cross_total['mean']
    traffic_total['mean'] = 0 if math.isnan(traffic_total['mean']) else traffic_total['mean']
    '''

    if q is not None:
        q.put(int(cross_total['mean']))
        q.put(int(traffic_total['mean']))
    return

if __name__ == '__main__':
    excluded_settings = ['model', 'CP', 'MCA', 'E', 'Bdn', 'Rts', 'RUNS']
    initialize_files()
    configs = read_config()
    sumo = input('Graphical Interface [y/N]: ')
    sumo = 'sumo-gui' if sumo == 'y' or sumo == 'Y' else 'sumo'
    counter = 0
    q = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    extra_configs = {'simul':False, 'multiplier':1, 'crossing_rate':6,'crossing_cars':1, 'congestion_rate':True, 'spawn_rate':1, 'simulation_index':"1"}
    # DEBUG: uncomment below line when testing with EB
    for settings in configs:
        settings['TV'] = str(settings['TV'])
        if not testSaveDir(settings):
            break
        processes = []
        time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        for i in range(int(settings["RUNS"])):
            p =multiprocessing.Process(target=sim, args=(settings, i, time, f'/usr/bin/{sumo}', lock, q, extra_configs)) # run simulations with "sim" function
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
        # Writes the output
        if int(settings['RUNS']) > 1:
            file_name = f'[MULTIRUN_{time}]' + settings['model']
            for s in settings.keys():
                if s not in excluded_settings:
                    file_name += '_' + s + ':' + str(settings[s])
            file_name += '|{}'
            cwt_file = open('data/' + file_name.format('cross-total') + '.txt', 'w')
            twt_file = open('data/' + file_name.format('traffic-total') + '.txt', 'w')
            # Note that you have to call Queue.get() for each item you want to return.
            while not q.empty():
                cwt = q.get()
                twt = q.get()
                cwt_file.write(str(cwt)+'\n')
                twt_file.write(str(twt)+'\n')
            cwt_file.close()
            twt_file.close()
            print(f'Cumulative results of runs saved as {file_name}')
            counter += 1
            print(f"Chunk {counter}/{len(configs)} finished")

    print("All done")
