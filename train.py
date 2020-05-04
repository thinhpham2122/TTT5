from TTT5 import TTT5
from agent import Agent
import numpy as np
import random


def get_state(board, player):
    return np.array([np.append(board, player)])


def get_next_state(board, player, ai):
    board_l = TTT5()
    for i in range(len(board)):
        board_l.board = list(board)
        board_l.player = player
        ret = board_l.play(i)

        if 'win' in ret:
            return None, ret
    board_l.board = board[:]
    board_l.player = player
    state = get_state(board, player)
    ret = board_l.play(np.argmax(ai.predict(state)))
    if 'invalid' in ret:
        empty_index = []
        for i in range(len(board)):
            if not board[i]:
                empty_index.append(i)
        ret = board_l.play(empty_index[random.randrange(len(empty_index))])
    next_board = board_l.board
    next_player = board_l.player
    return get_state(next_board, next_player), ret


def get_reward(ret, next_ret):
    if 'win' in ret:
        return 1
    elif 'invalid' in ret or 'win' in next_ret:
        return -1
    else:
        return 0


def get_id(state):
    mem_id = ''
    for i in state[0]:
        mem_id += str(i + 1)
    return mem_id


def get_next_node(state, model):
    board = state[0][:-1]
    player = state[0][-1]
    nodes = []
    node_ids = []
    rewards = []

    new_board = TTT5()
    for i in range(len(board)):

        if board[i]:  # invalid moves
            nodes.append(None)
            node_ids.append(None)
            rewards.append(-1)
            continue

        new_board.board = list(board)
        new_board.player = player
        ret = new_board.play(i)
        if 'draw' in ret or 'win' in ret:
            nodes.append(None)
            node_ids.append(None)
            rewards.append(get_reward(ret, ''))

        else:
            next_state, next_ret = get_next_state(new_board.board[:], int(new_board.player), model)
            reward = get_reward(ret, next_ret)
            if 'win' in next_ret or 'draw' in next_ret:
                nodes.append(None)
                node_ids.append(None)
                rewards.append(reward)
            else:
                nodes.append(Node(next_state, None, None))
                node_ids.append(get_id(next_state))
                rewards.append(reward)
    return nodes, rewards, node_ids


def run():
    student = Agent(26, 25, model_name=name)
    game_n = 0
    while True:
        games = 25 if student.epsilon <= student.epsilon_min else 5000
        for g in range(games):
            board = TTT5()
            end = False
            game_n += 1
            turn = 0
            print(game_n, 'tree:', len(student.tree), student.epsilon, end='\r')
            while not end:
                player_turn = int(board.player)
                current_board = board.board[:]
                state = get_state(current_board, player_turn)
                current_node_id = get_id(state)

                if turn == 0:
                    action = game_n % 25
                else:
                    action = student.act(np.array(state))

                ret = board.play(action)
                reward = get_reward(ret, '')
                if not (current_node_id in student.tree) or g % 1000 == 0:
                    next_nodes, rewards, next_node_ids = get_next_node(state, student.model)
                    current_node = Node(state, rewards, next_node_ids)

                    student.add_node(current_node_id, current_node)
                    for node_id, node in zip(next_node_ids, next_nodes):
                        if node_id:
                            student.add_node(node_id, node)

                if g == 0:
                    print(f'{game_n}: {action} {ret} reward: {reward}')
                    board.print_board()

                if 'invalid' in ret:
                    break
                if 'win' in ret or 'draw' in ret:
                    end = True
                turn += 1
            # for node in student.tree:
            #     print(node)
            #     print(student.tree[node].state[0][:-1].reshape((5,5)))
            #     print(student.tree[node].reward)
            # exit()
        student.exp_replay()
        test = get_state([0]*25, 1)
        start_move = np.argmax(student.model.predict(test))
        student.model.save(f'keras_model/{name}_{str(int(game_n))}_{int(start_move)}')


class Node:
    def __init__(self, state, rewards, next_node_ids):
        self.state = state
        self.rewards = rewards
        self.next_node_ids = next_node_ids


name = 'h'
run()
