import math
import os
# import time
# from tkinter.messagebox import NO
import time

import numpy as np

from core_gameplay import local_to_global, global_to_local, valid_moves, valid_moves_3x3_global

MAX = math.inf
MIN = -math.inf

NUM_OF_SMALL_WINS = 0
NUM_OF_SMALL_LOSSES = 0

EMPTY_SPACE = 0
JONILO_MARKER = 1
OPPONENT_MARKER = 2

LOSS = -5
DRAW = 0
WIN = 5

BIG_BOARD_REP_LOSS = -100
BIG_BOARD_REP_DRAW = 0
BIG_BOARD_REP_WIN = 100

BOARD = np.zeros((9, 9), dtype=int)
BIG_BOARD_REP = np.zeros(9, dtype=int)

WIN_INDICES = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [0, 4, 8],
               [6, 4, 2],
               [0, 3, 6],
               [1, 4, 7],
               [2, 5, 8]]


# main function
def main():
    # loop to check if there is a jonilo.go file
    # if there is, then read the move_file and make the move
    # if there is not, then wait for jonilo.go file to be created
    # once jonilo.go file is created, then read the move_file and make the move
    # then write to the move_file
    # then delete jonilo.go file
    # then wait for jonilo.go file to be created
    # repeat
    exists = False
    while True:
        if os.path.exists("jonilo.go"):
            exists = True
        if exists:
            # check if move_file is empty
            if os.stat("move_file").st_size == 0:
                # if it is empty, then write to move_file
                get_last_move_and_board("first_four_moves")
                # os.remove("jonilo.go")
                exists = False
            else:
                # if it is not empty, then read the move_file and make the move
                get_last_move_and_board("move_file")
                # os.remove("jonilo.go")
                exists = False


def get_last_move_and_board(file_name_to_open):
    with open(file_name_to_open, "r") as fp:
        # Get last non-empty line from file
        line = ""
        for next_line in fp.readlines():
            if next_line.isspace():
                break
            else:
                line = next_line
                current_position = line.split()
                if current_position[0] == "jonilo":
                    BOARD[int(current_position[1])][int(current_position[2])] = JONILO_MARKER
                else:
                    BOARD[int(current_position[1])][int(current_position[2])] = OPPONENT_MARKER

    # Tokenize move
    tokens = line.split()

    if len(tokens) > 0:
        if tokens[0] != "jonilo":
            print("tokens: " + file_name_to_open + " " + str(tokens))
            # Get board and location
            board_num = int(tokens[1])
            location_num = int(tokens[2])

            # Convert to global coordinates
            global_location_num = local_to_global([board_num, location_num])

            # Write to move file
            # board location is the last local location that was played
            write_to_move_file(BOARD, location_num)
        else:
            return
    else:
        return False


def minimax_decision(board, local_board_to_play):
    # get all valid moves
    valid_moves_list = valid_moves(board, local_board_to_play, False)
    valid_moves_list_3x3 = []
    #print(valid_moves_list)
    #time.sleep(1)

    for moves in valid_moves_list:
        local_move = global_to_local(moves)
        local_move.reverse()
        valid_moves_list_3x3.append(local_move)

    if not valid_moves_list_3x3:
        print("empty valid moves shouldn't happen")

    bestValue = MIN
    bestCoord = [MIN, MIN]

    for i in range(9):
        for j in range(9):
            state = board

            if state[i][j] == EMPTY_SPACE:

                state[i][j] = JONILO_MARKER
                value = minimax_value(0, state, False, MIN, MAX, local_board_to_play)

                if value > bestValue and [i, j] in valid_moves_list_3x3:
                    bestCoord = [i, j]
                    bestValue = value

                state[i][j] = EMPTY_SPACE
    print(f"Best Coordinate: {bestCoord}")
    board[bestCoord[0]][bestCoord[1]] = JONILO_MARKER
    return bestCoord


def minimax_value(depth, board, isMaxPlayer, alpha, beta, local_board_to_play):
    moves = []
    if local_board_to_play == -1:
        for i in range(0, 9):
            moves += valid_moves_3x3_global(board[i], i, isMaxPlayer)
        score = util_function(BIG_BOARD_REP)
    else:
        moves = valid_moves_3x3_global(board[local_board_to_play], local_board_to_play, isMaxPlayer)
        score = eval_function(board, local_board_to_play)

    if not moves:
        return util_function(BIG_BOARD_REP)

    # if not valid_moves_3x3_global(board, local_board_to_play, isMaxPlayer):
    #     score = util_function(board)
    # else:
    #     score = eval_function(board, isMaxPlayer)
    # Implement DRAW and BAD_MOVE cases

    if depth == 1:
        return score

    if isMaxPlayer:
        V = MIN
        for i in range(9):
            for j in range(9):
                # Create a temporary board so main board does not have issues
                state = board

                if state[i][j] == EMPTY_SPACE:
                    # JONILO_MARKER most likely needs to change
                    state[i][j] = JONILO_MARKER
                    val = minimax_value(depth + 1, state, False, alpha, beta, local_board_to_play)
                    V = max(V, val)

                    alpha = max(alpha, V)
                    state[i][j] = EMPTY_SPACE

                    # This might need to be in the first loop and not second
                    if beta <= alpha:
                        break

        # print(V)
        return V

    else:
        V = MAX
        for i in range(9):
            for j in range(9):
                # Create a temporary board so main board does not have issues
                state = board

                if state[i][j] == EMPTY_SPACE:
                    # OPPONENT_MARKER most likely needs to change
                    state[i][j] = OPPONENT_MARKER
                    val = minimax_value(depth + 1, state, True, alpha, beta, local_board_to_play)
                    V = min(V, val)

                    beta = min(beta, V)
                    state[i][j] = EMPTY_SPACE

                    if beta <= alpha:
                        break
        # print(V)
        return V


def util_function(board):
    # This is going to be a function that given a terminal global board returns the number of points won by the
    # current player
    # Check if there is a check for global board if not we have to implement it ourselves

    if EMPTY_SPACE not in board:
        return DRAW
    else:
        for indices in WIN_INDICES:
            if board[indices[0]].any() == JONILO_MARKER and \
                    board[indices[1]].any() == JONILO_MARKER and \
                    board[indices[2]].any() == JONILO_MARKER:
                return BIG_BOARD_REP_WIN

            elif board[indices[0]].any() == OPPONENT_MARKER and \
                    board[indices[1]].any() == OPPONENT_MARKER and \
                    board[indices[2]].any() == OPPONENT_MARKER:
                return BIG_BOARD_REP_LOSS

    return DRAW


def eval_function(board, local_board_to_play):
    # Add heuristic function here
    # Evaluates non-terminal global board configs
    # Must coincide (be equal to) util_function on terminal global board configs
    # This also might have to change
    # all_valid_moves = valid_moves_3x3_global(board, local_board_to_play, False)
    # convert to local coordinates

    global NUM_OF_SMALL_WINS
    global NUM_OF_SMALL_LOSSES

    if EMPTY_SPACE not in board:
        return DRAW

    elif is_small_center(board, local_board_to_play, JONILO_MARKER) or is_in_center(board, JONILO_MARKER):
        return 3

    elif is_small_center(board, local_board_to_play, OPPONENT_MARKER) or is_in_center(board, OPPONENT_MARKER):
        return -3

    else:
        for indices in WIN_INDICES:
            if board[local_board_to_play][indices[0]].any() == JONILO_MARKER and \
                    board[local_board_to_play][indices[1]].any() == JONILO_MARKER and \
                    board[local_board_to_play][indices[2]].any() == JONILO_MARKER:

                # mark the BIG_BOARD_REP with the winner
                BIG_BOARD_REP[local_board_to_play] = JONILO_MARKER
                if util_function(BIG_BOARD_REP) == BIG_BOARD_REP_WIN:
                    return BIG_BOARD_REP_WIN

                NUM_OF_SMALL_WINS += 1

                if local_board_to_play == 4:
                    return 10

                return WIN

            elif board[local_board_to_play][indices[0]].any() == OPPONENT_MARKER and \
                    board[local_board_to_play][indices[1]].any() == OPPONENT_MARKER and \
                    board[local_board_to_play][indices[2]].any() == OPPONENT_MARKER:

                BIG_BOARD_REP[local_board_to_play] = OPPONENT_MARKER
                if util_function(BIG_BOARD_REP) == BIG_BOARD_REP_LOSS:
                    return BIG_BOARD_REP_LOSS

                NUM_OF_SMALL_LOSSES += 1

                if local_board_to_play == 4:
                    return -10

                return LOSS

    return NUM_OF_SMALL_WINS - NUM_OF_SMALL_LOSSES


def is_small_center(board, local_board_to_play, marker):
    if board[local_board_to_play][4].any() == marker:
        return True
    return False


def is_in_center(board, marker):
    for i in range(9):
        if board[4][i].any() == marker:
            return True
        return False


def write_to_move_file(board, local_board_to_play):
    move_file = open("move_file", "r+")
    # We will want to change this to whatever move that ab pruning finds the most beneficial
    best_coord = minimax_decision(board, local_board_to_play)
    move_file.seek(0)
    move_file.write(f"jonilo {str(best_coord[0])} {str(best_coord[1])}\n")
    move_file.truncate()
    move_file.close()


def move_file_output(board):
    output = ""
    agentName = "Jonilo"
    boardNum = 2
    locationNum = 2
    i = 0

    while i < 4:
        output += agentName + " " + str(boardNum) + " " + str(locationNum) + " "
    return output


if __name__ == "__main__":
    main()
