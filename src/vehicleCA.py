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
        # base model sampled between 0 and beta, now it's deterministic.
        # each car will have a different beta though.
        # each vehicle has a R% prob of chosing a random beta
        beta = self.settings['Spn'] * 0.01
        UB = int((self.settings['betaU'])*100)
        LB = int((self.settings['betaL'])*100)
        R = self.settings['betaR']
        if self.settings['TV'] != self.getID():
            if np.random.rand() <= R:
                beta = (random.choice([i for i in range(LB, UB+1)]))/100
                # print("RANDOM BETA: {}".format(str(beta)))
            else:
                beta = (int(self.getID()) % (UB-LB+1)+LB)/100
        # print("veic = {} beta = {}".format(self.getID(), beta))
        return int(self.getBudget() * beta)
