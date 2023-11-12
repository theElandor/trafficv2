from src.utils import *
from src.vehicleAbstract import *

class VehicleAuction(VehicleAbstract):

    def __init__(self, id, settings, variable_pool):
        super().__init__(id, settings, variable_pool)
        self.budget = self.max_budget
        self.crossroad_counter = self.countCrossroads()
        self.lazy_refill = False

    def setLabel(self):
        """
        'State' parameter of traci vehicle is used to label graphically them in the GUI with a custom value
        """
        traci.vehicle.setParameter(self.id, 'State', self.budget)
        return

    def reroute(self):
        super().reroute()
        return

    def makeBid(self):
        """
        dependently on given bidding policy, returns a random bid or a thoughtful bid partitioned for the crossroads to pass
        :return:
        bid, made from the vehicle for its auction
        """
        # self.route is route
        # veic.getRouteIndex() to get current index
        if self.settings['Bdn'] == 'b':
            current_road = traci.vehicle.getRoadID(self.getID())
            current_index = self.managedLanes.index(current_road)
            rem = self.crossroad_counter-current_index
            to_bid = self.getBudget()/rem
            return to_bid
        else:
            return randint(0, int(self.getBudget()))

    def setBudget(self, budget):
        if budget >= 0:
            self.budget = int(budget)
        self.setLabel()

    def getBudget(self):
        return self.budget
