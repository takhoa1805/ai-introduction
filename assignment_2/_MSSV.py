import math
import numpy as np
from state import State, State_2



def evaluate(state):
    if state.game_over:
        if state.game_result(state.global_cells.reshape(3, 3)) == state.X:
            return 100
        elif state.game_result(state.global_cells.reshape(3, 3)) == state.O:
            return -100
        else:
            return 0
    score = 0
    for i in range(9):
        result = state.game_result(state.blocks[i])
        if result == state.X:
            score += 10
        elif result == state.O:
            score -= 10
    return score

def minimax(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or state.game_over:
        return evaluate(state)
    
    if maximizing_player:
        max_eval = -math.inf
        for move in state.get_valid_moves:
            new_state = State(state)
            new_state.act_move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in state.get_valid_moves:
            new_state = State(state)
            new_state.act_move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def select_move(cur_state, remain_time):
    best_move = None
    best_value = -math.inf if cur_state.player_to_move == 1 else math.inf
    valid_moves = cur_state.get_valid_moves

    print('valid_moves',valid_moves)
    for move in valid_moves:
        new_state = State(cur_state)
        new_state.act_move(move)
        board_value = minimax(new_state, 3, -math.inf, math.inf, cur_state.player_to_move == -1)
        if cur_state.player_to_move == 1:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move

    print('best_move',best_move)

    return best_move
