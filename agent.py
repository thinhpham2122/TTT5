from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam

import numpy as np
import random
from collections import deque


rotate_location = [4, 9, 14, 19, 24, 3, 8, 13, 18, 23, 2, 7, 12, 17, 22, 1, 6, 11, 16, 21, 0, 5, 10, 15, 20]


def rotate(board):
    rotated_board = []
    for location in rotate_location:
        rotated_board.append(int(board[location]))
    if len(board) > 25:
        rotated_board.append(int(board[25]))
    return rotated_board


def get_rotate_boards(s, t):
    states, targets = [], []
    for i in range(len(s)):
        os = s.pop()
        ot = t.pop()
        states.append(os[:])
        targets.append(ot[:])
        for rotation in range(3):
            os = rotate(os)
            ot = rotate(ot)
            states.append(os[:])
            targets.append(ot[:])
    return states, targets


def get_conv2d_input(states):
    inputs = []
    for state in states:
        broad = np.array(state[:25]).reshape((5, 5))
        player = np.full((5, 5), state[-1])
        inputs.append([broad, player])
    return np.array(inputs)


class Node:
    def __int__(self, state, reward, next_node_id):
        self.state = state
        self.reward = reward
        self.next_node_id = next_node_id


class Agent:
    def __init__(self, state_size, action_size, model_name=None):
        self.state_size = state_size
        self.action_size = action_size
        self.tree = {}
        self.model_name = model_name
        self.gamma = 0.95
        self.data = 3_000_000
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
        model.add(Conv2D(64, (3, 3), input_shape=(5, 5, 2), padding='valid', activation='relu'))
        model.add(Conv2D(64, (3, 3), padding='valid', activation='relu'))
        model.add(Flatten())
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        model.summary()
        return model

    def act(self, state, print_allow):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            if random.random() <= self.epsilon:
                if print_allow:
                    print('Random')
                empty_index = []
                board = []
                for i, loc in enumerate(state.flatten()):
                    if i % 2 == 0:
                        board.append(loc)
                for i in range(25):
                    if not board[i]:
                        empty_index.append(i)
                return empty_index[random.randrange(len(empty_index))]

        output = self.model.predict(state)
        if print_allow:
            print('Predict')
            print(output[0].reshape((5, 5)))
        return np.argmax(output)

    def exp_replay(self):
        states = []
        targets = []
        next_states = []

        for node_id in self.tree:
            node = self.tree[node_id]
            if node.rewards:
                states.append(node.state[0])
                targets.append(node.rewards)

                for next_node_id in node.next_node_ids:
                    if next_node_id:
                        next_states.append(self.tree[next_node_id].state[0])

        next_outputs = deque(self.model.predict(np.array(next_states), verbose=1))

        state_n = -1
        for node_id in self.tree:
            node = self.tree[node_id]
            if node.rewards:
                state_n += 1
                for i, next_node_id in enumerate(node.next_node_ids):
                    if next_node_id:
                        targets[state_n][i] = min(max(max(next_outputs.popleft()), -1), 1)
                # print(node.state[0][:-1].reshape((5, 5)))
                # print(np.array(targets[state_n]).reshape((5, 5)))
                # print('')
        # states, targets = get_rotate_boards(states, targets)
        # states = get_conv2d_input(states)
        self.model.fit([states], [targets], epochs=1, verbose=1, batch_size=8192)

    def add_node(self, node_id, node):
        if node_id in self.tree:
            if node.rewards:
                self.tree[node_id] = node
        else:
            self.tree[node_id] = node
