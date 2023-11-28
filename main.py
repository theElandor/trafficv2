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
    var = settings['Vr']
    if var == 'NBB':
        var = 'B'
    folder_name = str(settings[var])
    model_version = settings['MV']
    simulation_index = str(settings['AI'])
    compared_path = "models/{}/compared_exp/average_{}T/".format(model_version, folder_name)
    final_path = "models/{}/compared_exp/average_{}T/{}".format(model_version, folder_name, simulation_index)
    # reminder prints
    print(compared_path)
    print(final_path)
    # create paths
    paths = [compared_path, final_path]
    for p in paths:
        if not os.path.exists(p):
            # uncomment for input confirmation
            # c = input("{} destination folder does not exist. Do you want to create it now? (y/n)".format(p))
            c = "y"
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
        
        excluded_settings = ['model', 'CP', 'MCA', 'E', 'Bdn', 'Rts', 'RUNS']
        log_file_initialization(chunk_name, settings, model_chosen, listener, time, excluded_settings)
        
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
        var = settings['Vr']
        if var == 'NBB':
            var = 'B'
        folder_name = str(settings[var])
        if model.test_veic != "?":
            with open("models/{}/compared_exp/average_{}T/{}/gained_{}.txt".format(settings['MV'], folder_name, str(settings['AI']), str(model.simulationName)), "w") as f:
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
    
    var = configs['Vr']
    if var == 'NBB':
        var = 'B'
    folder_name = str(configs[var])
    
    crossroad_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/crossroad_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    traffic_vehicles.to_csv("./models/{}/compared_exp/average_{}T/{}/traffic_{}.txt".format(configs['MV'], folder_name, str(configs['AI']), str(simulationName)),header=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    
    print(OKGREEN + f'Raw data written in data/{chunk_name}[{time}]{configs["model"]}|*.txt' + ENDC)

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
    print("Need to run {} simulations. Estimated time: {} hours.".format(len(configs), str("%02d:%02d" % (divmod((len(configs)*6)/5, 60)))))
    sumo = input('Graphical Interface [y/N]: ')
    sumo = 'sumo-gui' if sumo == 'y' or sumo == 'Y' else 'sumo'
    counter = 0
    q = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    extra_configs = {'simul':False, 'multiplier':1, 'crossing_rate':6,'crossing_cars':1, 'congestion_rate':True, 'spawn_rate':1, 'simulation_index':"1"}
    # DEBUG: uncomment below line when testing with EB
    parallel = 5
    chunks = [configs[x:x+parallel] for x in range(0, len(configs), parallel)]
    for c in chunks:  # c is new configs
        processes = []
        time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        for i, settings in enumerate(c):
            settings['TV'] = str(settings['TV'])
            if not testSaveDir(settings):
                break
            p =multiprocessing.Process(target=sim, args=(settings, i, time, f'/usr/bin/{sumo}', lock, q, extra_configs))  # run simulations with "sim" function
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
    print("All done")
