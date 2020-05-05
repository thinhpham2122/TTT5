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
        self.data = 10_000_000
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
                mem = self.tree[mem_id]
                mask = (mem[0][0][:-1] == 0)
                flip = sum(mem[1]) - mem[1]
                prob = flip * mask / sum(flip)
                if p:
                    print('Explore')
                    print(np.array(prob).reshape((5, 5)))
                return np.where(np.random.multinomial(1, prob))[0][0], None

            if p:
                print('Random')
            empty_index = []
            for i in range(25):
                if not state[0][i]:
                    empty_index.append(i)
            return empty_index[random.randrange(len(empty_index))], None

        if mem_id in self.tree:
            mem = self.tree[mem_id]
            q = np.nan_to_num(mem[2] / mem[1])
            if p:
                print('Max Q')
                print(q.reshape((5, 5)))
            return np.argmax(q), None

        if len(self.memory) >= 5_000_000:
            if p:
                print('Predict leaf')
            output = self.model.predict(state)
            return None, output[0][-1]
        else:
            if p:
                print('Random')
            empty_index = []
            for i in range(25):
                if not state[0][i]:
                    empty_index.append(i)
            return empty_index[random.randrange(len(empty_index))], None

    def exp_replay(self):
        self.make_tree()
        states = []
        targets = []
        for mem_id in self.tree:
            states.append(self.tree[mem_id][0][0])

        # targets = self.model.predict(np.array(states), verbose=1)
        for i, mem_id in enumerate(self.tree):
            mem = self.tree[mem_id]
            targets.append(np.append(mem[1] / sum(mem[1]), max(np.nan_to_num(mem[2]/mem[1]))))
            # print(mem[0][0][:-1].reshape((5,5)))
            # print(targets[-1])

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
                counters = np.zeros(self.action_size-1)
                rewards = np.zeros(self.action_size-1)
                counters[action] = 1
                rewards[action] = reward
                for i, location in enumerate(state[0][:-1]):
                    if location:
                        counters[i] = 1
                        rewards[i] = -1
                self.tree[mem_id] = [state, counters, rewards]
