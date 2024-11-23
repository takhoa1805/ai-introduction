import numpy as np
from state import State, State_2


def select_move(cur_state, remain_time):
    def minimax(state, depth, maximizing_player):
        if depth == 0 or state.game_over:
            return evaluate(state)
        
        if maximizing_player:
            max_eval = -np.inf
            for move in state.get_valid_moves:
                child_state = State(state)
                # if not state.is_valid_move(move) and not child_state.is_valid_move(move):
                if not child_state.is_valid_move(move):
                    continue
                try:
                    child_state.act_move(move)
                except:
                    print("error catched")
                    continue
                eval = minimax(child_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = np.inf
            for move in state.get_valid_moves:
                child_state = State(state)
                # if not state.is_valid_move(move) and not child_state.is_valid_move(move):
                if not child_state.is_valid_move(move):
                    continue
                try:
                    child_state.act_move(move)
                except:
                    print("error catched")
                    continue
                eval = minimax(child_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(state):
        if state.game_result(state.global_cells.reshape(3, 3)) == state.X:
            return 1
        elif state.game_result(state.global_cells.reshape(3, 3)) == state.O:
            return -1
        else:
            return 0

    best_move = None
    best_value = -np.inf
    for move in cur_state.get_valid_moves:
        child_state = State(cur_state)
        # child_state.act_move(move)

        # if not cur_state.is_valid_move(move) and not child_state.is_valid_move(move):
        if not child_state.is_valid_move(move):
            continue
        try:
            child_state.act_move(move)
        except:
            print("error catched")
            continue
        move_value = minimax(child_state, 3, False)  # Depth can be adjusted
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move
