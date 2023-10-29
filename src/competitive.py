from src.intersectionManager import *
import math

#basically the same as cooperative, but sponsorship is implemented.
class Competitive(IntersectionManager):

    def bidSystem(self, crossroad_stop_list, traffic_stop_list):
        #input: cars waiting at the head of the crossing, cars waiting in line.
        #output: winning veichle that has the right to use the crossing.
        bids = []
        sponsorships = defaultdict(list)

        for car in crossroad_stop_list:

            sponsorship = 0

            # Collecting sponsorships
            if self.settings['Spn'] > 0:
                for sp in traffic_stop_list[car.getRoadID()]:
                    tip = sp.makeSponsor()
                    print('bidSystem: vehicle {} receives a sponsorship of {} from vehicle {}'.format(car.getID(), tip, sp.getID()))
                    sponsorship += tip
                    sp.setBudget(sp.getBudget() - tip)

            car_bid = car.makeBid() + 1

            if self.settings['E'] == 'y':
                # logarithm of all vehicles in traffic in the given lane, +1 (vehicle at head of the queue, not in traffic list)
                # +1 for having something always >= 1 (ln of 1 is 0)
                enhance = math.log(len(traffic_stop_list[car.getRoadID()]) + 1) + 1
            else:
                enhance = 1

            total_bid = int((car_bid + sponsorship) * enhance)
            bids.append([car, total_bid, car_bid, sponsorship, enhance])
            log_print('bidSystem: vehicle {} has a total bid of {} (bid {}, enhancement {}, sponsorship {})'.format(car.getID(), total_bid, car_bid, enhance, sponsorship))
            # sponsorship is added to car bid to find the car with more bid (sponsorship included)

        bids, winner, winner_total_bid, winner_bid, winner_enhance = self.sortBids(bids)

        winner.setBudget(winner.getBudget() - winner_bid + 1)
        log_print('bidSystem: vehicle {} pays {} and wins the auction (new budget of {})'.format(winner.getID(), winner_bid-1, winner.getBudget()))
        self.bidPayment(bids, winner_bid)

        win = [bids[0][0]]
        return win
