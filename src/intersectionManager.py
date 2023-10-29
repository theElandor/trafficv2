from src.utils import *
from operator import itemgetter

from src.vehiclesDict import VehiclesDict

class IntersectionManager:

    def __init__(self, settings):
        self.settings = settings

    def intersectionControl(self, crossroad):        
        """
        Method inherited from any class that expands 'IntersectionManager' class.
        Vehicles near the crossroad are collected and stored in two separated lists, one for vehicles participating
        auction, one for the vehicles stationary for traffic conditions.
        A vehicle that is about to participate in an auction has its traffic waiting time collected and stored (if any), then
        it starts clocking time spent for auction. To notice that crossroads are managed sequentially, but idle time is
        set simultaneously with traffic waiting time of vehicles, so there is no need to start it in advance.
        :param crossroad: instance of 'Crossroad' representing the crossroad to be managed
        :param listener: instance of 'StepListener' used to control the simulation status (if step limit is reached)
        :return:
        """

        crossroad_stop_list, traffic_stop_list = self.collectWaitingVehicles(crossroad)
        #calls bid systems (who calls sort_bids) and returns ordered cars that will depart.
        if len(crossroad_stop_list) >= self.settings['MCA']: # MCA: "Minimum cars for auctions"
            log_print('intersectionControl: enough cars in crossroad_stop_list, auction starts...')
            assert len(crossroad_stop_list) <= 4

            idle_time = crossroad.getIdleTime()
            for v in crossroad_stop_list:
                log_print('intersectionControl: vehicle {} invocation of \'getTimePassedInTraffic\' at crossroad {} with idle time {}'.format(v.getID(), crossroad.getName(), idle_time))
                v.getTimePassedInTraffic(crossroad.getName(), idle_time)
                log_print('intersectionControl: vehicle {} invocation of \'setCrossroadWaitingTime\''.format(v.getID()))
                v.setCrossroadWaitingTime()

            # bidSystem is declared only in sub-models (to avoid use of this generic model instead of specialized ones).
            departing_cars = self.bidSystem(crossroad_stop_list, traffic_stop_list, crossroad)
            log_print('intersectionControl: idle_time set at {}'.format(idle_time))
            crossroad.resetIdleTime()
            log_print('intersectionControl: \'resetIdleTime\' invocation for crossroad {}'.format(crossroad.getName()))

            return departing_cars, idle_time, traffic_stop_list

        elif 0 < len(crossroad_stop_list) < self.settings['MCA']:
            crossroad.setIdleTime()
            log_print('intersectionControl: crossroad {} \'setIdleTime\' invocation'.format(crossroad.getName()))
            for c in traffic_stop_list.keys():
                for veh in traffic_stop_list[c]:
                    log_print('intersectionControl: vehicle {} invocation of \'getTimePassedInTraffic\' with time_passed of {}'.format(veh.getID(), veh.getTimePassedInTraffic(crossroad.getName(), crossroad.getIdleTime())))
        elif len(crossroad_stop_list) == 0:
            log_print('intersectionControl: crossroad {} \'resetIdleTime\' invocation'.format(crossroad.getName()))
            crossroad.resetIdleTime()
        return [], 0, []

    def collectWaitingVehicles(self, crossroad):
        #input: crossroad
        #output: (i) crossroad_stop_list --> veichles stopped at the fron of the lane, waiting to cross
        #        (ii) traffic_stop_list --> veichles waiting in traffic (so waiting in line, behind veics in crossroad_stop_list)
        crossroad_stop_list = []
        traffic_stop_list = defaultdict(list) #defaultdict is a dict that never raises a KeyError for keys that are not in the dict itself.
        for v in VehiclesDict.vd.values(): #for each veichle
            road = traci.vehicle.getRoadID(v.getID()) #gets the road
            if traci.vehicle.isStopped(v.getID()) and road in crossroad.getInEdges():
                crossroad_stop_list.append(v)
            # if vehicles is stationary (NOT stopped) and near the considered crossroad, it is considered "in traffic"
            elif traci.vehicle.getSpeed(v.getID()) < 2 and traci.vehicle.getRoadID(v.getID()) in crossroad.getInEdges():                
                traffic_stop_list[v.getRoadID()].append(v)                
                v.setTrafficWaitingTime()            
        assert (len(crossroad_stop_list) <= 4)
        for key in traffic_stop_list:
            #ordering veics waiting in traffic for each road.
            traffic_stop_list[key] = sorted(traffic_stop_list[key], key=lambda item : traci.vehicle.getLanePosition(item.getID()), reverse=True)
        return crossroad_stop_list, traffic_stop_list
    
    def sortBids(self, bids, sponsors):
        bids = list(reversed(sorted(bids, key=itemgetter(1))))
        #bids[0] = winner
        winner = bids[0][0]
        winner_total_bid = bids[0][1]
        winner_bid = bids[0][2] - sponsors[winner]
        winner_enhance = bids[0][3]
        log_print('sortBids: winner is vehicle {} with a \'total bid\' of {}'.format(winner.getID(), winner_total_bid))
        return bids, winner, winner_total_bid, winner_bid, winner_enhance

    def bidPayment(self, bids, winner_bid):
        """
        Redistributes winner money to auction partecipants, also
        in cooperative approach.
        """
        for i in range(1, len(bids)):
            #re-distributes winner's bid to other veichles
            bids[i][0].setBudget(bids[i][0].getBudget() + round(winner_bid / (len(bids) - 1)))
            log_print('bidPayment: vehicle {} receives {} (new budget {})'.format(bids[i][0].getID(), round(winner_bid / (len(bids) - 1)), bids[i][0].getBudget()))

        if self.settings['CP'] == 'avp': ## all veichles pay
            # range starts from '1' to skip first position (whom is the winner, always charged of its bid)
            for i in range(1, len(bids)):
                # +1 is added to avoid a vehicle to completely exhaust its budget
                bids[i][0].setBudget(bids[i][0].getBudget() - bids[i][1] + 1)
                log_print('bigPayment: vehicle {} pays {} (new budget {})'.format(bids[i][0].getID(), bids[i][1] - 1, bids[i][0].getBudget()))

    def bidSystem(self, crossroad_stop_list, traffic_stop_list, crossroad): ## has to be implemented by subclasses
        pass
