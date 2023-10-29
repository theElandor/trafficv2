import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate, Embedding, Reshape, Flatten
from tensorflow.keras import Sequential
import numpy as np
import random
from keras import layers
from collections import deque
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import initializers
import gc
import sys
import os

class LossHistory(keras.callbacks.Callback):
    
    """
    Class used to store the values of the loss function
    overtime. With reinforcement learning using the loss
    function to see if the model converges is not a good idea,
    because the target network always changes, so it will
    be really instable. Plotting either the reward or
    the expected Q value is a better idea.
    """
    
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

class Agent:

    """
    Agent class. It is a wrapper for the model that
    needs to be trained. Contains many utility functions,
    and is responsible for the training(fitting) procedure.
    """

    def __init__(self, settings):

        """
        Initialization of some internal variables.
        """

        self.activation = 'relu'
        self.loss = 'mse'
        self.action_size = 11  # index between 0 and 10
        self.experience_replay = deque()
        self.train = settings['train']
        self.load = settings['load']
        # change this to load a different model
        self.model_version = settings['MV']
        self.optimizer = Adam(learning_rate=0.00001)
        self.q_path = os.path.dirname(__file__) + "/../models/"+str(self.model_version)+"/q-network"
        self.target_path = os.path.dirname(__file__) + "/../models/"+str(self.model_version)+"/target-network"
        self.exploration_epsilon = settings['EXE']
        self.evaluation_epsilon = settings['EVE']

        """
        Initialization of some hyperparameters.
        The following are the values used to train the "hope" model.

        self.batch_size = 32
        self.gamma = 0.3
        """
        self.batch_size = settings['BS']
        self.gamma = settings['G']

        if not self.load:
            self.q_network = self._build_model()
            self.target_network = self._build_model()
        else:
            self.set_evaluation_epsilon()
            self.load_model(self.q_path, self.target_path)

    def save(self):
        """
        Method that saves the weights of both target net and q net.
        """
        self.q_network.save("q-network")
        self.target_network.save("target-network")
    def set_exploration_epsilon(self):
        """
        Used when memory is still less big than batch size
        """
        self.epsilon = self.exploration_epsilon
    def set_evaluation_epsilon(self):
        """
        Used when memory size is bigger than batch size
        and the model is trying to get new examples in memory
        """
        self.epsilon = self.evaluation_epsilon
    def load_model(self, q_path, target_path):
        """
        Method that loads the models from specified paths
        INPUT:
        q_path: path of q_network
        target_path: path of target_network
        """
        self.q_network = keras.models.load_model(q_path)
        self.target_network = keras.models.load_model(target_path)

    def _build_model(self):
        """
        Model that builds the structure of the neural network.
        """

        model = Sequential()
        # add model layers
        model.add(Dense(128, activation='relu', input_shape=(9,),kernel_initializer=initializers.RandomNormal(stddev=0.15),bias_initializer=initializers.Zeros()))
        model.add(Dense(128, activation='relu', kernel_initializer=initializers.RandomNormal(stddev=0.15),bias_initializer=initializers.Zeros()))
        model.add(Dense(128, activation='relu', kernel_initializer=initializers.RandomNormal(stddev=0.15),bias_initializer=initializers.Zeros()))
        model.add(Dense(self.action_size, activation=self.activation))
        model.compile(optimizer=self.optimizer, loss=self.loss)
        return model

    def remember(self, state, action, reward, next_state):
        """
        Function used to fill the experience replay with new data.
        The training procedure will randomly sample data from the experience replay.
        """
        self.experience_replay.append((state, action, reward, next_state))

    def act(self, state):
        """
        This function takes in input the state of the environment and outputs either:
        - the index of the highest Q-value
        - a random index
        So it chooses between exploitation and exploration.
        Some debug prints are present.
        """
        q_values = self.q_network.predict(state, verbose=0)
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            with open("actions.txt", "a") as a:
                a.write("{}\n".format(str(action)))
            print("Q-VALUES: " + str(q_values))
            print("PICKING action with index:  " + str(action))
            return action
        with open("Q-values.txt", "a") as qv:
            qv.write("{}\n".format(np.max(q_values[0])))
        print("Q-VALUES: " + str(q_values))
        gc.collect()
        keras.backend.clear_session()
        action = np.argmax(q_values[0])
        print("PICKING action with index:  " + str(action))
        with open("actions.txt", "a") as a:
            a.write("{}\n".format(str(action)))
        return action

    def update_target_model(self):
        """
        Function that sets the target-network equal to the q-network.
        Reed thesis for more info on this.
        """
        self.target_network.set_weights(self.q_network.get_weights())

    def retrain(self):

        """
        Function that handles the training. Randomly samples batch_size
        elements from the experience replay and applies backpropagation
        to train the q-network.
        """

        batch = random.sample(self.experience_replay, self.batch_size)

        # for each example in the batch
        for state, action, reward, next_state in batch:
            # q-learn rule is applied
            prediction = self.q_network.predict(state, verbose=0)
            target = self.target_network.predict(next_state, verbose=0)
            prediction[0][action] = reward + self.gamma * np.amax(target)
            # saving loss for convergence analysis.
            history = LossHistory()
            # allenamento della rete
            self.q_network.fit(state, prediction, epochs=1, callbacks=[history])
            with open("loss.txt", "a") as f:
                for n in history.losses:
                    f.write(str(n) + "\n")
        # commands used to cleanup memory
        gc.collect()
        keras.backend.clear_session()
