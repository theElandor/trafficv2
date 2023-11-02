from src.vehicleAuction import VehicleAuction
import numpy as np
import random


class VehicleCA(VehicleAuction):
    def makeSponsor(self):
        """
        for 'Competitive' approach, sponsorships consists in a bid participation to help the head of the queue, in order
        to speed traffic flow in that lane
        :return:
        sponsorship randomly picked, according to set sponsorship percentage
        """
        # now the random beta is not a thing anymore. Every vehicle can have either
        # a fixed policy among all simulations or a random one. The random consists
        # in initializing a beta randomly in the given range
        return int(self.getBudget() * self.beta)
