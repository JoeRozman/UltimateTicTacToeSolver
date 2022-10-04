import math
import os
# import time
# from tkinter.messagebox import NO

import numpy as np

from core_gameplay import local_to_global, global_to_local, valid_moves, valid_moves_3x3_global

MAX = math.inf
MIN = -math.inf

EMPTY_SPACE = 0
JONILO_MARKER = 1
OPPONENT_MARKER = 2

LOSS = -1
DRAW = 0
WIN = 1
BIG_BOARD_REP_WIN = 10
BOARD = np.zeros((9, 9), dtype=int)
BIG_BOARD_REP = np.zeros((9), dtype=int)

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
        print("tokens from first_four_moves: " + str(tokens))
        # Get board and location
        board_num = int(tokens[1])
        location_num = int(tokens[2])

        # Convert to global coordinates
        global_location_num = local_to_global([board_num, location_num])

        # Write to move file
        # board location is the last local location that was played
        write_to_move_file(BOARD, location_num)
    else:
        return False


def minimax_decision(board, local_board_to_play):
    # get all valid moves
    valid_moves_list = valid_moves(board, local_board_to_play, False)
    valid_moves_list_3x3 = []

    for moves in valid_moves_list:
        local_move = global_to_local(moves)
        local_move.reverse()
        valid_moves_list_3x3.append(local_move)

    bestValue = -2
    bestCoord = [-1, -1]
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
    # print(board)
    return bestCoord


def minimax_value(depth, board, isMaxPlayer, alpha, beta, local_board_to_play):
    moves = []
    if local_board_to_play == -1:
        for i in range(0, 9):
            moves += valid_moves_3x3_global(board[i], i, isMaxPlayer)
        score = eval_function(board, local_board_to_play)
    else:
        moves = valid_moves_3x3_global(board[local_board_to_play], local_board_to_play, isMaxPlayer)
        score = eval_function(board, local_board_to_play)

    if not moves:
        return util_function(board)

    if score == BIG_BOARD_REP_WIN:
        return WIN

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

    if EMPTY_SPACE not in BIG_BOARD_REP:
        return DRAW
    else:
        for indices in WIN_INDICES:
                if BIG_BOARD_REP[indices[0]].any() == JONILO_MARKER and \
                        BIG_BOARD_REP[indices[1]].any() == JONILO_MARKER and \
                        BIG_BOARD_REP[indices[2]].any() == JONILO_MARKER:
                    return BIG_BOARD_REP_WIN

    return DRAW


def eval_function(board, local_board_to_play):
    # Add heuristic function here
    # Evaluates non-terminal global board configs
    # Must coincide (be equal to) util_function on terminal global board configs
    # This also might have to change
    # all_valid_moves = valid_moves_3x3_global(board, local_board_to_play, False)
    # convert to local coordinates
    if EMPTY_SPACE not in board:
        return DRAW
    else:
        # print(board[WIN_INDICES[0][0]])
        for indices in WIN_INDICES:
            if board[indices[0]].any() == board[indices[1]].any() and \
                    board[indices[1]].any() == board[indices[2]].any() and \
                    board[indices[0]].any() != EMPTY_SPACE:
                # mark the BIG_BOARD_REP with the winner
                BIG_BOARD_REP[local_board_to_play] = JONILO_MARKER
                if util_function(BIG_BOARD_REP.any()) == BIG_BOARD_REP_WIN:
                    return BIG_BOARD_REP_WIN
                return WIN

    return DRAW


def write_to_move_file(board, local_board_to_play):
    move_file = open("move_file", "r+")
    # We will want to change this to whatever move that ab pruning finds the most beneficial
    best_coord = minimax_decision(board, local_board_to_play)
    move_file.seek(0)
    move_file.write("jonilo" + " " + str(best_coord[0]) + " " + str(best_coord[1]) + "\n")
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
