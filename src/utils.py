#Auxiliary class with used methods, to slim code of "main.py"
from distutils.command.config import config
import os

from prettytable import PrettyTable
import re
import traci
from collections import defaultdict
import pandas as pd
import yaml
from subprocess import Popen, PIPE, STDOUT
from LinkedList import ListNode
import numpy as np


from src.vehicleCA import VehicleCA
from src.vehicleDA import VehicleDA
from src.vehicleEB import VehicleEB
from src.crossroad import Crossroad
from src.utility_print import *
from src.vehiclesDict import VehiclesDict
from src.CrossGraph import Graph

pt = PrettyTable()
log_file = ""
l = ""

"""
prompt the user to chose which model using for simulation
"""

def read_config():
    output = Popen("find configs/ -wholename \'*.yml\'", shell=True, stdout=PIPE)
    config_files = str(output.stdout.read()).removeprefix('b\'').removesuffix('\'').removesuffix('\\n').split('\\n')

    pt.field_names = ['#', 'File']
    pt.align['File'] = 'l'
    for c in config_files:
        pt.add_row([config_files.index(c) + 1, c])

    os.system('clear')
    print(pt)
    selector = 0
    pt.clear()

    files_to_read = []
    if selector == 0:
        files_to_read = config_files
    else:
        files_to_read.append(config_files[selector-1])

    configs = []
    for f in files_to_read:
        f = f.removeprefix("\"").removeprefix("\'").removesuffix("\"")
        with open(f, "r") as ymlfile:
            configs.append(yaml.load(ymlfile, Loader=yaml.FullLoader))
    return configs

def manual_config(models):
    model_chosen = modelSelection(models)
    configs = simulationSettings(model_chosen)
    # configs is encapsulated and returned as a list because in read_config the configurations of all the yml files read are stored in this way
    return [configs]

def modelSelection(models):
    """
    Asks the user to choose for the model to use in the simulation
    :param models: list of available models
    :return:
    """
    pt.field_names = ['#', 'Model']
    pt.align['Model'] = 'l'
    for m in models:
        pt.add_row([models.index(m) + 1, m])

    selector = 0
    while selector < 1 or selector > len(models):
        os.system('clear')
        print(pt)
        try:
            selector = int(input(BOLD + 'Choose model to use: ' + ENDC))
        except:
            print(FAIL + 'Wrong input. Retry' + ENDC)
            continue

    pt.clear()
    return models[selector - 1]


def simulationSettings(model_chosen):
    """
    Asks the user the specific settings for the model chosen, checking their correctness
    models:
        Coop = Cooperative
        Comp = Competitive
        EB = Emergent Behavior
    settings:
        CP = Crossing Policy
        MCA = Minimum Cars for Auction
        E = Enhancement
        Bdn = Bidding
        Spn = Sponsorship
        IF = Increasing Function
        IC = Increasing Coefficient
        DF = Decreasing Function
        DC = Decreasing Coefficient
        SF = Spreading Function
        SR = Spreading Range
        DM = Distance Magnitude
        SP = Spreading Polarity
        Rts = Routes
        Stp = Steps
        VS = Vehicles to Spawn
    values:
        wp / ap = Crossing Policy (winner pays / all pay)
        y / n = Enhancement (yes / no)
        b / r = Bidding (balanced / random)
        lin / log / gro = Increasing (or Decreasing) Function (linear / logarithmic / grower)
        std / dbl / rbl = Spreading Function (standard exchange / distance-based logarithmic / range-based logarithmic)
        op / an = Spreading Polarity (only positive / allow negative)
        f / r = Routes (fixed / random)

    :param model_chosen: string representing the model to use
    :return:
    """
    options = []
    values = []
    if model_chosen == 'Coop' or model_chosen == 'Comp':
        options = ['CP', 'MCA', 'E']
        values = ['owp', 2, 'y']
    if model_chosen == 'Coop' or model_chosen == 'Comp' or model_chosen == 'DA':
        options.append('Bdn')
        values.append('b')
    if model_chosen == 'Comp':
        options.append('Spn')
        values.append(50)
    elif model_chosen == 'EB':
        options = ['IF', 'IC', 'DF', 'DC', 'SF', 'SR',
                   'DM', 'SP']
        values = ['lin', 10, 'lin', 10, 'std', 100, 10.0, 'an']

    # 'Steps' and 'Vehicles to spawn are common settings
    options.append('Rts')
    values.append('f')

    options.append('Stp')
    values.append(10000)

    options.append('VS')
    values.append(100)

    options.append('RUNS')
    values.append(1)

    menu_fields = options.copy()
    for f in range(len(menu_fields)):
        menu_fields[f] = menu_fields[f] + " [" + str(f + 1) + "]"  # indices start from '1'
    pt.field_names = menu_fields
    change_setting = -1

    while change_setting != '':
        os.system('clear')
        # settings values are updated in Pretty Table, leaving unaltered fields names
        pt.clear_rows()
        pt.add_row(values)
        print(pt)
        try:
            change_setting = input('To change settings, type [index] or press Enter: ')
            if change_setting == '':
                break
            change_setting = int(change_setting) - 1  # -1 because indices of list started from '0', not '1'
        except:
            change_setting = -1

        if 0 <= change_setting < len(options):
            os.system('clear')
            # Crossing Policy
            if options[change_setting] == 'CP':
                try:
                    crossing_sel = int(input('Available crossing policies:\n'
                                             '[1] winner-pays\n'
                                             '[2] all-vehicles-pay\n'
                                             'Select: '))
                except:
                    continue
                if crossing_sel == 1:
                    values[change_setting] = 'owp'
                elif crossing_sel == 2:
                    values[change_setting] = 'avp'
                continue

            # Minimum number of cars for an auction
            if options[change_setting] == 'MCA':
                try:
                    min_cars = int(input("Enter minimum number of cars you want to make an auction(2~4): "))
                except:
                    continue
                if 1 <= min_cars <= 4:
                    values[change_setting] = min_cars
                continue

            # Enhancement
            if options[change_setting] == 'E':
                try:
                    enhancement = input("Do you want to enable enhancement? [Y/n]: ")
                except:
                    continue
                if enhancement != 'N' and enhancement != 'n':
                    values[change_setting] = 'y'
                else:
                    values[change_setting] = 'n'
                continue

            # Route typology
            if options[change_setting] == 'Rts':
                try:
                    fixed_routes = input("Do you want fixed routes (otherwise, random ones)? [Y/n]: ")
                except:
                    continue
                if fixed_routes != 'N' and fixed_routes != 'n':
                    values[change_setting] = 'f'
                else:
                    values[change_setting] = 'r'
                continue

            # Bidding type
            if options[change_setting] == 'Bdn':
                try:
                    balance_bidding = input('Do you want to enable balanced bidding (otherwise, random bidding)? [Y/n]: ')
                except:
                    continue
                if balance_bidding != 'N' and balance_bidding != 'n':
                    values[change_setting] = 'b'
                else:
                    values[change_setting] = 'r'
                continue

            # Sponsorship (only for competitive)
            if options[change_setting] == 'Spn':
                try:
                    sponsorship = int(input("Enter maximum percentage for sponsorship [default: 50%]: "))
                except:
                    continue
                if 0 <= sponsorship <= 100:
                    values[change_setting] = sponsorship
                else:
                    values[change_setting] = 50
                continue

            # Simulation steps
            if options[change_setting] == 'Stp':
                try:
                    step_to_stop = int(input("How many steps the simulation should do? [default: 0, infinite steps]: "))
                except:
                    step_to_stop = 0
                if step_to_stop > 0:
                    values[change_setting] = step_to_stop
                continue

            # Vehicles number
            if options[change_setting] == 'VS':
                try:
                    vehicles_to_spawn = int(input("How many vehicles should be spawned? [default: 100]: "))
                except:
                    vehicles_to_spawn = 100
                if vehicles_to_spawn > 0:
                    values[change_setting] = vehicles_to_spawn
                continue

            # Simulation RUNS
            if options[change_setting] == 'RUNS':
                try:
                    runs = int(input("How many runs should be made? [default: 1]: "))
                except:
                    runs = 1
                if runs > 0:
                    values[change_setting] = runs
                continue

            # Incr./Decr. function for Hurry
            if options[change_setting] == 'IF' or options[change_setting] == 'DF':
                try:
                    function = int(input('Available functions:\n'
                                         '[1] linear\n'
                                         '[2] logarithmic\n'
                                         '[3] grower\n'
                                         'Select: '))
                except:
                    continue
                if function == 1:
                    values[change_setting] = 'lin'
                elif function == 2:
                    values[change_setting] = 'log'
                elif function == 3:
                    values[change_setting] = 'gro'
                continue

            # Incr./Decr. coefficient for Hurry
            if options[change_setting] == 'IC' or options[change_setting] == 'DC':
                try:
                    coefficient = int(input('Insert coefficient for the chosen function: '))
                except:
                    continue
                if 0 < coefficient:
                    values[change_setting] = coefficient
                continue

            # Spreading Function
            if options[change_setting] == 'SF':
                try:
                    function = int(input('Available functions:\n'
                                         '[1] standard exchange \n'
                                         '[2] distance-based logarithmic\n'
                                         '[3] range-based logarithmic\n'
                                         'Select: '))
                except:
                    continue
                if function == 1:
                    values[change_setting] = 'std'
                elif function == 2:
                    values[change_setting] = 'dbl'
                elif function == 3:
                    values[change_setting] = 'rbl'
                continue

            # Spreading range
            if options[change_setting] == 'SR':
                try:
                    coefficient = int(input('Insert spreading range: '))
                except:
                    continue
                if coefficient >= 0:
                    values[change_setting] = coefficient
                continue

            # Distance Magnitude
            if options[change_setting] == 'DM':
                try:
                    coefficient = float(input('Insert distance magnitude: '))
                except:
                    continue
                if 0 < coefficient:
                    values[change_setting] = coefficient
                continue

            # Spread Type
            if options[change_setting] == 'SP':
                try:
                    function = int(input('Available kind of spread:\n'
                                         '[1] only-positive \n'
                                         '[2] allow-negative \n'
                                         'Select: '))
                except:
                    continue

                if function == 1:
                    values[change_setting] = 'op'
                elif function == 2:
                    values[change_setting] = 'an'
                continue

    pt.clear()
    options.append('model')
    values.append(model_chosen)
    configs = {options[i]: values[i] for i in range(len(options))}
    if model_chosen == 'EB':
        configs['MCA'] = 1
    return configs


def retrieveCrossroadsNames():
    """
    Use a specific regular expression to retrieve crossroads to be handled during the simulation
    :return: set of crossroads names retrieved
    """
    crossroads_names = set()
    crossroad_pattern = r"^(?!:)[ABCDEFGHI].*"
    for c in traci.junction.getIDList():
        if re.match(crossroad_pattern, c):
            crossroads_names.add(c)
    return crossroads_names


def infrastructureRetrieving(crossroad_names):
    """
    Collects, using traci API, elements in the simulation (edges and crossroads)
    :param crossroad_names: names of crossroads to manage specifically
    :return:
    'crossroads': dictionary associating, for each name of crossroad, the corresponding 'Crossroad' instance
    'edges': list of edges in the environment
    'in_edges': sub-list of edges going IN a crossroad
    """
    crossroads = {}
    edges = []
    edge_pattern = r"^(?!:).+"
    in_edge_pattern = r"edge(.)+[ABCDEFGHI]"
    in_edges = defaultdict(list)  # it's a defaultdict to avoid required initialization of the list for each crossroad
    # Get all edges from traci
    for i in traci.edge.getIDList():
        # store all of them into corresponding set...
        if re.match(edge_pattern, i):
            edges.append(i)
        # and edges entering a crossroad (ends with an alphabet letter) are stored in a dictionary, with each key referring to a list of edges going in that crossroad
        if re.match(in_edge_pattern, i):
            in_edges[str(i[len(i) - 1])].append(i)

    for i in crossroad_names:
        crossroads[i] = Crossroad(i, in_edges[i], traci.junction.getPosition(i))

    return crossroads, edges, in_edges

#offset is needed when vehicles are spawned overtime,
#to see changes according to traffic flow.
def createPool(settings):
    total = settings['VS']
    percentage = settings['RS']  # random spawn
    variable_pool = [str(i) for i in range(1, int(total*(percentage/100)))]
    return variable_pool

def spawnCars(settings, routes, offset=0):
    """
    Spawn the requested cars into the scenario
    :param cars_to_spawn: number of cars to be spawn
    :param settings: dictionary containing current simulation settings, to be passed in each 'Vehicle' instance
    :return: dictionary of 'Vehicle' instances, labeled with given ID
    """
    cars_to_spawn = settings['VS']
    variable_pool = createPool(settings)
    congestion = True
    for i in range(cars_to_spawn):
        # print("Spawning car: " + str(i+offset))
        traci.vehicle.add(str(i+offset), routes[(i+offset) % len(routes)])
        traci.simulationStep()
        if settings['model'] == 'Comp' or settings['model'] == 'Coop':
            VehicleCA(str(i+offset), settings, variable_pool)
        if settings['model'] == 'EB':
            VehicleEB(str(i), settings, congestion)
        if settings['model'] == 'DA':
            VehicleDA(str(i), settings)
        # Vehicles created are automatically added to VehiclesDict
    return

def departCars(settings, dc, idle_times, listener, in_edges, out_edges,extra_configs,traffic,non_players = []):
    """
    Depart specified cars from respective crossroads, handling Traffic Waiting Time and Crossroad Waiting Time
    :param settings: dictionary containing configuration of current simulation
    :param dc: dictionary {crossroad : cars} of vehicles that have to depart from respective crossroad
    :param idle_times: dictionary containing, for each crossroad, idle_time to be curtailed from waiting times
    :param listener: 'StepListener' used to check simulation status (step limit is respected)
    :return:
    """
    waiting = {}
    veicDict = {}
    crossing_cars = extra_configs['crossing_cars']
    crossing_rate = extra_configs['crossing_rate']
    for crossroad in dc.keys():
        waiting[crossroad]=[]
        for veic in dc[crossroad]:
            waiting[crossroad].append(veic.getID())
            veicDict[veic.getID()] = veic
    trajectories = {}
    if extra_configs['simul']:
        for crossroad in dc.keys():
            trajectories[crossroad] = checkRoutes(dc, crossroad, in_edges, out_edges, log=True)    
    for i in range(crossing_cars):
        to_resume = []
        for crossroad in dc.keys():
            if i < len(dc[crossroad]) and dc[crossroad][i].getID() in waiting[crossroad]: # and i < mass[crossroad]
                waiting[crossroad].remove(dc[crossroad][i].getID()) # remove departed veichle from waiting list.
                #make other cars with non intercepting trajectoried depart
                #followers contains also contains the current veichle departing
                followers = []
                current = dc[crossroad][i].getID() # ID of current veichle departing from crossing
                index = dc[crossroad][i].getRouteIndex()
                current_start = dc[crossroad][i].getRoute()[index]
                current_direction = dc[crossroad][i].getRoute()[index+1]
                if extra_configs['simul']:
                    starting_node = trajectories[crossroad][current_start]
                followers.append(current)
                if current not in non_players and extra_configs['simul']:  # if it is a aut. driven veic, then we can look for more aut.veics that can cross together
                    for candidate in waiting[crossroad]:  # for each other waiting veichle
                        iterator = starting_node
                        if candidate not in non_players:
                            while True:  # need to emulate do-while loop
                                if [v for v in followers if v in [g.getID() for g in iterator.occ]] and candidate in [g.getID() for g in iterator.occ]:
                                    break
                                else:
                                    iterator = iterator.next
                                    if iterator == starting_node:
                                        followers.append(candidate)
                                        break
                to_resume.append(current)  # traci.vehicle.resume(current)
                with open("flow.txt", "a") as flow:
                    flow.write(current + "," + crossroad + "\n")
                log_print('departCars: vehicle {} is departing from crossroad {}'.format(current, crossroad))
                log_print('departCars: vehicle {} invocation of \'getTimePassedAtCrossroad\' with time_passed of {}'.format(current, dc[crossroad][i].getTimePassedAtCrossroad(crossroad, idle_times[crossroad])))
                dc[crossroad][i].resetCrossroadWaitingTime()
                log_print('departCars: vehicle {} invocation of \'resetCrossroadWaitingTime\''.format(current))
                for j in range(1, len(followers)):
                    print("APPENDED")
                    to_resume.append(followers[j])
                    # we add veic to to_resume list instead of eparting it immead.
                    # traci.vehicle.resume(followers[j])                    
                    log_print('departCars: vehicle {} is departing from crossroad {}'.format(followers[j], crossroad))
                    log_print('departCars: vehicle {} invocation of \'getTimePassedAtCrossroad\' with time_passed of {}'.format(followers[j], veicDict[followers[j]].getTimePassedAtCrossroad(crossroad, idle_times[crossroad])))
                    waiting[crossroad].remove(followers[j])
                    veicDict[followers[j]].resetCrossroadWaitingTime()
                    #we should reset the crossroad w.t of every car that leaves the crossing
                    log_print('departCars: vehicle {} invocation of \'resetCrossroadWaitingTime\''.format(followers[j]))
        for resume_car in to_resume:
            traci.vehicle.resume(resume_car)
            if veicDict[resume_car].lazy_refill:
                veicDict[resume_car].gained_money += veicDict[resume_car].getBudget()
                veicDict[resume_car].setBudget(veicDict[resume_car].max_budget)
                veicDict[resume_car].managedLanes = [item for item in veicDict[resume_car].route if item in veicDict[resume_car].managedLanes]
                veicDict[resume_car].lazy_refill = False
        for i in range(crossing_rate):  # simulation steps
            traci.simulationStep()


def collectWT(crossroads_names):
    """
    Collects vehicles' waiting times (traffic and crossroad), divided for crossroad, and store in a common DataFrame.
    DataFrame is then accessed and elaborated on different representations (i.e. traffic and crossroad waiting times)
    :param vehicles: dictionary of vehicles used in the simulation, to be accessed to retrieve waiting times
    :param crossroads_names: list of crossroad names to use to access at each sub-list of each vehicle
    :return:
    df_waiting_time: DataFrame containing raw data
    cross_total: statistics summarizing ALL AUCTION waiting times measured
    traffic_total: statistics summarizing ALL TRAFFIC waiting times measured
    crossroads_wt: statistics summarizing respective AUCTION waiting times, divided for each CROSSROAD
    traffic_wt: statistics summarizing respective TRAFFIC waiting times, divided for each CROSSROAD
    crossroad_vehicles: statistics summarizing AUCTION waiting times, divided for each VEHICLE
    traffic_vehicles: statistics summarizing TRAFFIC waiting times, divided for each VEHICLE
    """
    df_waiting_times = pd.DataFrame(columns=['id', 'crossroad', 'crossroad_waiting_time', 'traffic_waiting_time'])
    for v in VehiclesDict.vd.values():
        v_wt = v.getCrossroadWaitedTimes()
        t_wt = v.getTrafficWaitedTimes()
        for c in crossroads_names:
            for wt in v_wt[c]:
                df_waiting_times = df_waiting_times.append(
                    {'id': int(v.getID()), 'crossroad': c, 'crossroad_waiting_time': float(wt)},
                    ignore_index=True)
            for wt in t_wt[c]:
                df_waiting_times = df_waiting_times.append(
                    {'id': int(v.getID()), 'crossroad': c, 'traffic_waiting_time': float(wt)}, ignore_index=True)

    cross_total = df_waiting_times.crossroad_waiting_time.describe()
    traffic_total = df_waiting_times.traffic_waiting_time.describe()
    crossroads_wt = df_waiting_times.groupby('crossroad').crossroad_waiting_time.describe()
    traffic_wt = df_waiting_times.groupby('crossroad').traffic_waiting_time.describe()
    crossroad_vehicles = df_waiting_times.groupby('id').crossroad_waiting_time.describe()
    traffic_vehicles = df_waiting_times.groupby('id').traffic_waiting_time.describe()
    return cross_total, traffic_total, df_waiting_times, crossroads_wt, traffic_wt, crossroad_vehicles, traffic_vehicles

def getOutEdges(in_edges):    # function that manipulates strings, to get out_edges. works only in sumo manhattan grid.        
    out_edges = defaultdict(list)
    for key in in_edges:
        out_edges[key] = []
        for edge in in_edges[key]:
            in_edge = edge
            in_edge = in_edge.removeprefix("edge")
            temp = in_edge.split("-")            
            out_edge = ""
            out_edge = "edge"+str(temp[1])+"-"+str(temp[0])
            out_edges[key].append(out_edge)
    return out_edges

def checkRoutes(dc, crossroad, in_edges, out_edges, log=False):    
    #first part creates a circular linked list to represent crossing
    crossroad_in_edges = in_edges[crossroad]
    crossroad_out_edges = out_edges[crossroad]
    starting_points = {}
    n = len(crossroad_in_edges)
    starting_points[crossroad_in_edges[0]] = ListNode(crossroad_out_edges[0])  
    for i in range(1,n):
        #create node and link to previous node
        starting_points[crossroad_in_edges[i]] = ListNode(crossroad_out_edges[i])
        starting_points[crossroad_in_edges[i-1]].next = starting_points[crossroad_in_edges[i]]
    #last->next = first, to create a circular list
    starting_points[crossroad_in_edges[n-1]].next = starting_points[crossroad_in_edges[0]]
    for veic in dc[crossroad]: #marks the nodes, based on trajectories of veics waiting in the crossing.
        index = veic.getRouteIndex()
        veic_start = str(veic.getRoute()[index])
        veic_end = str(veic.getRoute()[index+1])
        pointer = starting_points[veic_start]
        while(pointer.val != veic_end):
            pointer.occ.append(veic)
            pointer = pointer.next
    return starting_points
