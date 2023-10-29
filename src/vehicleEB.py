from src.vehicleAutonomous import VehicleAutonomous
from src.crossroad import Crossroad
from src.crossroadsDict import CrossroadsDict
from src.utility_print import *

import re
import traci
import numpy as np
from math import *

class VehicleEB(VehicleAutonomous):

    def __init__(self, id, settings, congestion) -> None:
        super().__init__(id, settings)
        self.hurry = 0
        self.hurry_contribution = 0
        self.corrected_hurry = 0
        self.congestion = congestion

    def action(self):
        self.applyContribution()
        self.changeHurry()
        
        for n in traci.lane.getLastStepVehicleIDs(traci.vehicle.getLaneID(self.getID())):
            if n != self.getID():
                distance = int(pow(pow(traci.vehicle.getPosition(n)[0] - self.getPosition()[0], 2) + (pow(traci.vehicle.getPosition(n)[1] - self.getPosition()[1], 2)), 0.5))
                if distance <= self.settings['SR']:
                    log_print('step: vehicle {} invocation of \'hurrySpreading\' (neighbor {}, at distance {})'.format(self.getID(), n, distance))        
                    self.hurrySpreading(float(traci.vehicle.getParameter(n, 'State')), distance) #uses normal hurry
    
        if traci.vehicle.getSpeed(self.getID()) < traci.vehicle.getAllowedSpeed(self.getID()) * 0.1:
            target_cr = traci.vehicle.getRoadID(self.getID()).split('-')[-1] # The last letter is the target crossroad (i.e. A)
            if traci.vehicle.isStopped(self.getID()):
                self.getTimePassedInTraffic(target_cr)
                self.setCrossroadWaitingTime()
                self.cross(target_cr)
            else:
                self.setTrafficWaitingTime()

        return 
    
    def cross(self, target_cr):
        re_crossroads = re.compile(rf"edge.*-{target_cr}")
        contenders = 0
        for c in CrossroadsDict.getGlobalInEdges():
            if re.match(re_crossroads, c):
                for v in traci.edge.getLastStepVehicleIDs(c):
                    if v != self.getID():
                        if traci.vehicle.isStopped(v):
                            contenders += 1
                            # if float(traci.vehicle.getParameter(v, 'State')) > self.getHurry():
                            # hurry influenced by congestion rate is used instead of normal hurry
                            if float(traci.vehicle.getParameter(v, 'CorrState')) > self.getCorrHurry():                                
                                break # you lost the comparison
                        
                # if the inner loop finished without 'break', it means you can continue to search, else you lost at least a confront and you can quit
                else:
                    continue
                break
        
        # you haven't found any vehicle with higher hurry for the same crossroad...
        else:
            # If there weren't other contenders, just reset the crossroad waiting timer 
            if contenders == 0:
                self.resetCrossroadWaitingTime()

            # if there were other contenders and you won, depart
            else:
                traci.vehicle.resume(self.getID())
                self.getTimePassedAtCrossroad(target_cr)
            return

        # if the loop has been broken, it means you lost the comparison and you need to wait
        return

    def setLabel(self):
        """
        'State' parameter of traci vehicle is used to label graphically them in the GUI with a custom value
        """
        traci.vehicle.setParameter(self.id, 'State', self.hurry)
        if self.congestion == False:        
            traci.vehicle.setParameter(self.id, 'CorrState', self.hurry)
        else:
            traci.vehicle.setParameter(self.id, 'CorrState', self.corrected_hurry)
        return

    def changeHurry(self):
        """
        Hurry is increased for each step in which the vehicle is stationary (speed is under 10% of maximal allowed) and decreased for each step in motion, applying the corresponding function with the given coefficient (increment and decrement are not necessarily symmetric).
        'contribution' stores the step update for the function to be applied
        'function' stores the kind of function to apply
        'polarity' stores the sign of the update (positive if its an increment, negative otherwise)
        :return:
        """

        if traci.vehicle.getSpeed(self.getID()) < traci.vehicle.getAllowedSpeed(self.getID()) * 0.1:
            contribution = float(self.settings['IC'])
            function = 'IF'
            polarity = 1
        else:
            contribution = float(self.settings['DC'])
            function = 'DF'
            polarity = -1

        # if function is 'linear', it's just the coefficient for the polarity
        if self.settings[function] == 'log':
            contribution *= log(self.hurry+2)
        elif self.settings[function] == 'gro':
            contribution = max(contribution * self.hurry/100, contribution)

        # hurry cannot be negative
        # self.hurry = max(self.hurry + int(contribution*polarity), 0)
        self.applyHurry(max(self.hurry + int(contribution*polarity), 0))
        return contribution
    
    def hurrySpreading(self, n_hurry, distance):
        """
        Given the hurry of the neighbor 'n' of current vehicle, in a 'distance' within the specified 'Range', apply the specified 'Spreading' function based on the difference between 'Hurry', restricted dependently by 'Spread Type' ('only-positive' and 'allow-negative').
        Computed 'contribution' is added to 'hurry_contribution', that is a container of the current influences received in that time step, to be applied in 'applyContribution' invocation, at the end of time step routine. Contribution isn't directly applied to allow "symmetric updating" (otherwise, two vehicles with the same 'Hurry' would have different reciprocal contributions dependently to their contribution computation).
        For computing correctly 'contribution', absolute value of 'diff' is considered (log of a negative number doesn't exist) and original sign is stored in 'polarity' parameter (+1 if it is an increment, -1 if it is a decrement).
        """
        diff = n_hurry - self.hurry

        # if diff is zero, quit now
        if diff == 0:
            return
        # if diff is negative, and only positive values are allowed, quit now
        if diff < 0 and self.settings['SP'] == 'op':
            return

        if self.settings['SF'] == 'std':
            contribution = diff / (distance * self.settings['DM'])
        elif self.settings['SF'] == 'dbl':
            # copysign is used to apply the original sign of diff to the contribution, otherwise abs(diff) would give only positive values
            contribution = log(abs(diff) + 1) * (distance * self.settings['DM']) * copysign(1, diff)
        elif self.settings['SF'] == 'rbl':
            contribution = log(abs(diff) + 1) * ((self.settings['SR'] * self.settings['DM']) / distance) * copysign(1, diff)  
        self.hurry_contribution += contribution
        return

    def applyContribution(self):
        """
        All contributions received in the current time step is applied, ensuring that 'Hurry' won't be negative, and resetting 'hurry_contribution' counter for the next time step
        :return:
        """
        self.applyHurry(max(self.hurry + int(self.hurry_contribution), 0))
        self.hurry_contribution = 0
    
    def getHurry(self):
        return self.hurry
    
    def getCorrHurry(self):
        if self.congestion == False:
            return self.hurry
        else:
            return self.corrected_hurry

    def applyHurry(self, hurry):
        if self.congestion == False:
            self.hurry = hurry
        else:
            self.hurry = hurry        
            current_route_position = traci.vehicle.getRouteIndex(self.id)
            next_route_position = traci.vehicle.getRoute(self.id)[current_route_position+1]
            cars_in_next_edge = len(traci.edge.getLastStepVehicleIDs(next_route_position))
            if cars_in_next_edge < 3:
                congestion_rate = 1 #congestion rate is not applied
            else:
                congestion_rate = (1/np.log(cars_in_next_edge))
            self.corrected_hurry = self.hurry * congestion_rate
