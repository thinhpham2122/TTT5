from TTT5 import TTT5
from agent import Agent
import numpy as np
import random


def get_state(board, player):
    if player == 1:
        state = board[:]
        state.append(-1)
    else:
        state = board[:]
        state.append(1)
    return np.array([state])


def get_next_state(board, player, ai):
    board_l = TTT5()
    for i in range(len(board)):
        board_l.board = board[:]
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


def get_events(state, board, player, ai):
    events_l = []
    win_action = []
    for i in range(len(board)):
        new_board = TTT5()
        new_board.board = board[:]
        new_board.player = player
        ret = new_board.play(i)
        if 'invalid' in ret or 'draw' in ret:
            reward = get_reward(ret, '')
            events_l.append([state, i, reward, None, True][:])
            continue
        elif 'win' in ret:
            win_action.append(i)
        else:
            next_state, next_ret = get_next_state(new_board.board[:], int(new_board.player), ai)
            reward = get_reward(ret, next_ret)
            if 'win' in next_ret or 'draw' in next_ret:
                events_l.append([state, i, reward, None, True][:])
            else:
                events_l.append([state, i, reward, next_state, False][:])
    if win_action:
        target = []
        for w in range(len(board)):
            if w in win_action:
                target.append(1)
            else:
                target.append(-1)
        return [state, target], 2
    return events_l, 1


def run():
    student = Agent(26, 25, model_name=name)
    game_n = 0
    while True:
        games = 25 if student.epsilon <= student.epsilon_min else 4000
        for _ in range(games):
            board = TTT5()
            end = False
            game_n += 1
            turn = 0
            print(game_n, len(student.memory), len(student.memory2), end='\r')
            while not end:
                player_turn = int(board.player)
                current_board = board.board[:]
                state = get_state(current_board, player_turn)
                if turn == 0:
                    action = game_n % 25
                else:
                    action = student.act(np.array(state))
                ret = board.play(action)
                events, mem_type = get_events(state, current_board, player_turn, student.model)
                if mem_type == 1:
                    student.memory.append(events)
                    reward = events[action][2]
                else:
                    student.memory2.append(events)
                    rewards = events[1]
                    reward = rewards[action]
                # print(f'{game_n}: {action} {ret} reward: {reward}')
                # board.print_board()
                if 'invalid' in ret:
                    break
                if 'win' in ret or 'draw' in ret:
                    end = True
                turn += 1
        student.exp_replay()
        test = get_state([0]*25, 1)
        start_move = np.argmax(student.model.predict(test))
        student.model.save(f'keras_model/{name}_{str(int(game_n))}_{int(start_move)}')



name = 'h'
run()
