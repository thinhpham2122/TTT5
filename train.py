from TTT5 import TTT5
from agent import Agent
import numpy as np
import random


def get_state(board, player):
    state = board
    state.append(player)
    return np.array([state])


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


def run():
    student = Agent(26, 26, model_name=name)
    game_n = 0
    while True:
        games = 25 if student.epsilon <= student.epsilon_min else 100000
        for g in range(games):
            board = TTT5()
            end = False
            game_n += 1
            turn = 0
            reward = 0
            tem_mem = []
            last_player = 0
            print(game_n, 'mem:', len(student.memory), 'tree:', len(student.tree), student.epsilon, end='\r')
            while not end:
                player_turn = int(board.player)
                current_board = board.board[:]
                state = get_state(current_board, player_turn)
                mem_id = get_id(state)
                action, value = student.act(np.array(state), mem_id, g == 0)
                if action != None:
                    ret = board.play(action)
                if value:
                    reward = value
                    last_player = player_turn
                    end = True
                    continue
                tem_mem.append([mem_id, state, action][:])
                if g == 0:
                    print(f'{game_n}: {action} {ret} reward: {reward}')
                    board.print_board()

                if 'invalid' in ret:
                    break

                elif 'win' in ret:
                    reward = 1
                    last_player = player_turn
                    end = True

                elif 'draw' in ret:
                    reward = 0
                    last_player = player_turn
                    end = True
                turn += 1

            for [mem_id, state, action] in tem_mem:
                player = state[0][-1]
                reward = reward if player == last_player else - reward
                student.memory.append([mem_id, state, action, reward])

        student.exp_replay()
        student.model.save(f'keras_model/{name}_{str(int(game_n))}')



name = 'MCST'
run()
