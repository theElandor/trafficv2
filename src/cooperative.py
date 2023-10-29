from src.intersectionManager import *
import math
import numpy as np
from src.bidder import Agent

class Cooperative(IntersectionManager):
    def __init__(self, settings, extra_configs):
        super().__init__(settings)
        self.multiplier = extra_configs["multiplier"]
        self.congestion_rate = extra_configs["congestion_rate"]
        
        """
        enable self.load if you want to load a model from the
        "models" directory. The model version is specified
        in the bidder class (bidder.py file). The current
        stable version of the model is named 'hope'
        """
        self.load = settings['load']
        self.train = settings['train']
        
        """
        IMPORTANT:
        simulationName is used to rename the output file. 'booster'
        is related to simulations where the bidder is active.
        'off' is used for the simulation used for comparison, so for
        the random bidder or for the normal behaviour.
        It is really important to use theese specific names or the
        plotters will not be able to read the output files (XD).
        """
        self.simulationName = settings['name']

        """
        simple saver is a configuration that never make sponsorships
        and always bet simple_discount*bid money in auctions.
        set self.simple_saver to true to enable it on the test veic.
        """
        
        self.simple_saver = False
        self.simple_discount = 0.3
        self.evaluation = False

        """
        max_memory parameter has been used during training.
        Not super usefull if you train for a reasonable amount
        of ticks (like 200k). If the training lasts for long,
        then it might be smart to set this parameter to
        limit the memory size.
        """
        self.max_memory = 400
        
        """
        The tests used veic 74 as the test vehicle. To "install" the bidder
        on a different vehicle just change the value of self.test_veic.
        Right now the simulator does not support multiple test vehicles,
        as they would require to either:
        1) Keep in memory a different model for each one;
        2) Keep in memory a single model for each test vehicle, but
           in this case they would need to have the same route.
        IMP
        If you want to disable the bidder, please just set the variable like this:
        self.test_veic = "?"
        """
        self.test_veic = settings['TV']
        """
        This parameter controls the importance of placing cheap bets.
        A value close to 0 will make the bidder receive more reward
        if it uses really high discounts, caring less about improving
        its position in traffic.
        The stable model uses alpha = 0.3;
        """
        self.alpha = settings['alpha']
        """
        self.freq is another hyperparameter. It controls after how
        many action steps the model should learn. If set to 1,
        then the "train" function is called every time that the
        agent performs an action, leading to a low variability in
        the training dataset.
        """
        self.train_freq = settings['TF']
        self.update_freq = settings['UF']
        self.E1 = 0.1
        self.E2 = 0.2
        self.E3 = 0.3
        
        """
        bidder initialization.
        """
        self.bidder = Agent(settings)

        """
        some internal variables initialization.
        """
        self.freeze = False
        self.sample = 0
        self.train_count = 0
        self.prev_state = []
        self.prev_action = []
        self.mapping = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7,
            "I": 8
        }
    def get_reward(self, prev_state, prev_action, current_state):

        """
        function that returns the value of the reward based on the current
        state of the environment and the prevoius state of the environment.
        state: [crossroad id, veic position]
        + crossroad id: numeric ID of the crossroad
        + veic position: veic position in lane (0: immediatly before crosser, -1 waiting to cross)
        reward: to be defined

        """
        # TODO: need to add bid value to minimize overall money spent
        print(prev_state, prev_action, current_state)
        prev_crossroad = prev_state[0][0]
        prev_position = prev_state[0][1]
        current_crossroad = current_state[0][0]
        current_position = current_state[0][1]

        discount = prev_action / 10  # [0, 0.1, 0.2, 0.3...1]
        position_reward = (prev_position - current_position)  # 1 if pos increased
        if prev_crossroad != current_crossroad:  # if veic crosses crossroad
            position_reward = 2
        final_reward = (self.alpha*(position_reward) + (1-self.alpha)*(1-discount))
        if prev_crossroad == current_crossroad and prev_position == current_position:
            final_reward = -0.3  # if veic does not move, reward is 0
        print("reward: " + str(final_reward))
        with open("reward.txt", "a") as f:
            f.write(str(final_reward)+"\n")
        return final_reward
    
    def encode(self, state):
        """
        Function that encodes the state using soft encoding.
        for example:
        q_len = 5 (so 5 veics are waiting behind the first one)
        our veic is in position 1, so --> -1 0 1 2 3 4
        where -1 is the veic waiting to cross, 1 is our veic
        [2,1] --> [0, 0,(6-2)/6, 0, 0, 0, 0, 0, 0]

        This sort of "normalization" has been done to keep the
        values of the tensor (input of the NN) < 1, which is
        usually a good thing to do. Would be nice to figure out
        a way to feed in more information about the traffic
        situation surrounding the test veic.
        """
        if len(state) == 0:
            return []
        print(state)
        encoding = [0 for i in range(9)]
        crossroad = state[0][0]
        position = state[0][1] + 1
        size = state[0][2] + 1
        value = (size-position)/size
        encoding[crossroad] = value
        return encoding

    def predict_bid(self, current_state_input):
        # current_state_input --> [[crossroad, position, len(dc)]]
        # need to convert current_state input into a format that is readable from the NN.
        current_state_input_encoded = np.array([self.encode(current_state_input)])
        prev_state_input_encoded = np.array([self.encode(self.prev_state)])
        
        if self.train:
            print("TESTING VEIC PREDICTING WITH THIS INPUT:")
            print(prev_state_input_encoded, current_state_input_encoded)
            if len(prev_state_input_encoded[0]):  # skips first prediction to avoid error
                reward = self.get_reward(self.prev_state, self.prev_action, current_state_input)
                if self.evaluation == False:  # always remember
                    self.bidder.remember(prev_state_input_encoded, self.prev_action, reward, current_state_input_encoded)
                else:
                    print("MEMORY: " + str(len(self.bidder.experience_replay)))
                    if len(self.bidder.experience_replay) < self.max_memory:
                        self.bidder.remember(prev_state_input_encoded, self.prev_action, reward, current_state_input_encoded)
                    else:
                        # freezes memory and sets epsilon
                        # so that the model always exploits, never explores
                        self.freeze = True
                        self.bidder.set_evaluation_epsilon()
                self.sample += 1
            memsize = len(self.bidder.experience_replay)
            if memsize < self.bidder.batch_size:
                self.bidder.set_exploration_epsilon()
                print("eps: "+str(self.bidder.epsilon))
            else:  # so if memory is full enough
                # setting different values of epsilon based on memory size.
                # a full memory needs less exploration, so the epsilon is really low.
                # when inserting examples in a full memory, FIFO policy is used.
                if memsize < self.max_memory/2:
                    self.bidder.epsilon = self.E3
                elif memsize > self.max_memory/2 and memsize < self.max_memory:
                    self.bidder.epsilon = self.E2
                else:
                    self.bidder.epsilon = self.E1
                print("eps: "+str(self.bidder.epsilon))
                if self.sample > self.train_freq:  # train once each 10 actions
                    self.sample = 0
                    self.train_count += 1
                    print("Training(" + str(self.train_count)+"/"+str(self.update_freq)+")")
                    self.bidder.retrain()
                    if self.train_count == self.update_freq:
                        print("UPDATING TARGET NETWORK")
                        self.train_count = 0
                        if not self.freeze:
                            self.bidder.update_target_model()
                        else:
                            print("Model is freezed, not updating")
        action = self.bidder.act(current_state_input_encoded)
        # saving current state and current action as class attributes,
        # so the next istance of the function call will be able to access
        # those parameters in order to compute the reward.
        self.prev_state = current_state_input
        self.prev_action = action
        return action

    def bidSystem(self, crossroad_stop_list, traffic_stop_list, crossroad):
        """
        function that handles bidding, uses many utility functions inherited by base class.

        input:
            crossroad           --> handled crossroad
            crossroad_stop_list --> cars waiting at the front of the lane,
            traffic_stop_list   --> cars waiting in line
        output:
            ordered list of cars that have to depart from the crossroad.
            the order is computed based on the bids.
        the rules for the test vehicle (the one on which the bidder is installed)
        are quite different from the other ones, because the discount needs to be 
        computed and applied. That's why you will often find statements like the
        following:
        "if v.getID() == test_veic then ...."
        """
        bids = []
        test_veic = self.test_veic
        sponsors = {}
        for v in VehiclesDict.vd.values():  # for each veichle
            if v.getID() == test_veic:  # only check test_veic
                road = traci.vehicle.getRoadID(v.getID())
                try:
                    position = traffic_stop_list[road].index(v)
                except ValueError:
                    position = -1
                current_state = [self.mapping[crossroad.name], position, len(traffic_stop_list[road])]
                current_state_input = np.array([current_state])
        for car in crossroad_stop_list:
            car_bid = int(car.makeBid())
            if car.getID() == test_veic:
                self.trained_veic = car
                if self.simple_saver:
                    car_bid = car_bid * self.simple_discount
                else:  # in this case veic uses the bidder to predict the best reward
                    bid_modifier = self.predict_bid(current_state_input)
                    discount = (bid_modifier / 10)  # discount will be between 0 and 1
                    car_bid = car_bid * discount  # apply discount to car bid
                    with open("bids.txt", "a") as bids_file:
                        bids_file.write(str(crossroad)+","+str(car_bid)+"\n")
                    print("test_veic bidded " + str(car_bid))
            # now that we have the bid of the vehicle, we want to collect
            # sponsorships for the cars behind the first one.
            # so this last part of code is all about sponsorship collection.
            sponsorship = 0
            if self.settings['Spn'] > 0:
                for sp in traffic_stop_list[car.getRoadID()]:
                    # tip = sp.getBudget()/sp.crossroad_counter before test veic bidded this way.
                    tip = sp.makeSponsor()
                    discounted_tip = tip  # if veic is not trained, then discounted_tip is the same as tip
                    if sp.getID() == test_veic:
                        if self.simple_saver:
                            discounted_tip = 0
                            # simlpe_saver does not tip during sponsorship
                        else:  # in this case test veic2 predicts best bid
                            with open("./encounters.txt", "a") as en:
                                en.write(crossroad.name + "," + str(len(traffic_stop_list[car.getRoadID()]))+"\n")
                                en.write(crossroad.name + "," + str(len(crossroad_stop_list))+"\n")
                            sponsor_modifier = self.predict_bid(current_state_input)
                            tip_discount = (sponsor_modifier / 10)
                            discounted_tip = tip * tip_discount  # apply discount to tip
                            print("Current state is: " + str(current_state))
                    sponsorship += discounted_tip  # add only discounted tip
                    sp.setBudget(sp.getBudget() - discounted_tip)  # decurt discounted tip
            car_bid += sponsorship
            sponsors[car] = sponsorship            
            log_print('bidSystem: vehicle {} made a bid of {}'.format(car.getID(), car_bid))
            if self.settings['E'] == 'y':
                enhance = self.multiplier*math.log(len(traffic_stop_list[car.getRoadID()]) + 1) + 1 ## get num of cars in the same lane and apply formula.
            else:
                enhance = 1
            total_bid = int(car_bid * enhance)
            bids.append([car, total_bid, car_bid, enhance])
            log_print('bidSystem: vehicle {} has a total bid of {} (bid {}, enhancement {})'.format(car.getID(), total_bid, car_bid, enhance))

        bids, winner, winner_total_bid, winner_bid, winner_enhance = self.sortBids(bids, sponsors)
        log_print('bidSystem: vehicle {} pays {}'.format(winner.getID(), winner_bid - 1))
        # if winner is trained veic, then we update the amount of money spent and saved
        winner.setBudget(winner.getBudget() - winner_bid)
        # REDISTRIBUTE winning bid without sponsorship
        sponsorship_winner = sponsors[winner]
        self.bidPayment(bids, winner_bid-sponsorship_winner)
        departing = []
        for b in bids:
            departing.append(b[0])  # appends departing cars in order and return them as a list.
        return departing
