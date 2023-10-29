from src.utils import *
from src.vehicleAbstract import *
from src.vehicleAuction import VehicleAuction
from src.vehicleAutonomous import VehicleAutonomous
from src.crossroadsDict import CrossroadsDict
from src.utility_print import *
from src.vehiclesDict import VehiclesDict

class VehicleDA(VehicleAuction, VehicleAutonomous):
    currentBid = 0
    priority = -1
    participated = False

    def __init__(self, id, settings):
        super().__init__(id, settings)
        traci.vehicle.setParameter(self.id, 'State', self.budget)

    def action(self):
        '''
        Here the decentralized vehicle should look for other cars going to its same crossroad, making bids, choosing a leader for the auction, ...
        '''
        self.setLabel()
        if self.currentBid == 0:
            # NOTE: a vehicle bidding a low value (i.e. because he has to cross many crossroads) could never pass in absence of Enhancement
            self.currentBid = self.makeBid()
            traci.vehicle.setParameter(self.getID(), 'currentBid', self.currentBid)
            # every time setBudget is invoked, setLabel() is automatically called
            self.setBudget(self.getBudget() - self.currentBid)
            log_print(f'Vehicle {self.id} made a bid of {self.currentBid}')

        if traci.vehicle.isStopped(self.getID()):
            current_edge = traci.vehicle.getRoadID(self.getID())
            target_cr = current_edge.split('-')[-1] # The last letter is the target crossroad (i.e. A)
            log_print(f'Vehicle {self.id} is stopped on edge {current_edge} and wants to cross {target_cr}')
            self.getTimePassedInTraffic(target_cr)
            self.setCrossroadWaitingTime()
            self.cross(current_edge, target_cr)
        elif traci.vehicle.getSpeed(self.getID()) < traci.vehicle.getAllowedSpeed(self.getID()) * 0.1:
            self.setTrafficWaitingTime()
        return

    def cross(self, current_edge, target_cr):
        re_crossroads = re.compile(rf"edge.*-{target_cr}")
        contenders = []
        log_print(f'Vehicle {self.id} has a priority of {self.priority}')
        if self.priority < 0:
            self.priority = 0
            for c in CrossroadsDict.getGlobalInEdges():
                if re.match(re_crossroads, c) and c != current_edge:
                    for v in traci.edge.getLastStepVehicleIDs(c):
                        if traci.vehicle.isStopped(v):
                            contenders.append(VehiclesDict.getVehicle(v)) 
                            self.participated = True
                            if contenders[-1].getCurrentBid() > self.currentBid:
                                log_print(f'Vehicle {self.id} won the comparison agains vehicle {v}')
                                self.priority += 1 # you lost the comparison, your crossing is postponed
                                continue # (with the next edge)

        log_print(f'Vehicle {self.id} has a participated value {self.participated}, a priority of {self.priority} and met {len(contenders)} contenders')
        if self.participated:
            if self.priority == 0:
                if len(contenders) > 0:
                    split_bid = int(self.currentBid/len(contenders))
                    for c in contenders:
                        c.setBudget(c.getBudget() + split_bid)
                        c.setParticipated()
                        c.setLabel()
                log_print(f'Vehicle {self.id} crosses {target_cr}')
                traci.vehicle.resume(self.getID())
                self.getTimePassedAtCrossroad(target_cr)
                self.currentBid = 0
                self.participated = False
                self.priority = -1
                return
        
        self.priority -= 1
        return
    
    def getCurrentBid(self):
        return self.currentBid

    def setParticipated(self):
        self.participated = True

    def setLabel(self):
        """
        'State' parameter of traci vehicle is used to label graphically them in the GUI with a custom value
        """
        traci.vehicle.setParameter(self.id, 'State', self.budget)
        return