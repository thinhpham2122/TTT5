from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

import numpy as np
import random
from collections import deque


class Agent:
    def __init__(self, state_size, action_size, model_name=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=5_000_000)
        self.tree = {}
        self.model_name = model_name
        self.gamma = 0.95
        self.data = 2_500_000
        self.epsilon = 1.0
        self.epsilon_min = .25
        self.epsilon_decay = float(np.e)**float(np.log(self.epsilon_min/self.epsilon)/self.data)
        print('stat:', self.data, self.epsilon_decay)
        if model_name:
            try:
                print('loading model')
                self.model = load_model(f'keras_model/{model_name}')
            except:
                print('fail to load model, creating new model')
                self.model = self.model()
        else:
            print('creating new model')
            self.model = self.model()

    def model(self):
        model = Sequential()
        model.add(Dense(units=512, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=512, activation="relu"))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=128, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

    def act(self, state, mem_id, p):
        self.epsilon *= self.epsilon_decay

        if self.epsilon > self.epsilon_min and random.random() <= self.epsilon:
            if mem_id in self.tree:
                if p:
                    print('u')
                mem = self.tree[mem_id]
                return np.argmin(mem[1])
            if p:
                print('random')
            empty_index = []
            for i in range(25):
                if not state[0][i]:
                    empty_index.append(i)
            return empty_index[random.randrange(len(empty_index))]

        if mem_id in self.tree:
            if p:
                print('q')
            mem = self.tree[mem_id]
            q = np.nan_to_num(mem[2] / mem[1])
            return np.argmax(q)

        if p:
            print('predict')
        output = self.model.predict(state)
        # print(np.round(output[0][0:5], 2))
        # print(np.round(output[0][5:10], 2))
        # print(np.round(output[0][10:15], 2))
        # print(np.round(output[0][15:20], 2))
        # print(np.round(output[0][20:25], 2))
        return np.argmax(output)

    def exp_replay(self):
        self.make_tree()
        states = []

        for mem_id in self.tree:
            states.append(self.tree[mem_id][0][0])

        targets = self.model.predict(np.array(states), verbose=1)
        for i, mem_id in enumerate(self.tree):
            mem = self.tree[mem_id]
            for c, counter in enumerate(mem[1]):
                if counter:
                    targets[i][c] = mem[2][c] / mem[1][c]

        # for s, t in zip(states, targets):
        #     print(s, t)
        self.model.fit([states], [targets], epochs=1, verbose=1, batch_size=8192)

    def make_tree(self):
        self.tree = {}
        for [mem_id, state, action, reward] in self.memory:
            if mem_id in self.tree:
                self.tree[mem_id][1][action] += 1
                self.tree[mem_id][2][action] += reward
            else:
                counters = np.zeros(self.action_size)
                rewards = np.zeros(self.action_size)
                counters[action] = 1
                rewards[action] = reward
                for i, location in enumerate(state[0][:-1]):
                    if location:
                        counters[i] = 10000000
                        rewards[i] = -10000000
                self.tree[mem_id] = [state, counters, rewards]
