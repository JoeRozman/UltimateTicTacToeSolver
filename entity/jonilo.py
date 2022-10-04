import math
import os
import time
from tkinter.messagebox import NO

import numpy as np

from core_gameplay import NO_MARKER, PLAYER0_MARKER, PLAYER1_MARKER, local_to_global, check_3x3_win, valid_moves, valid_moves_3x3_global

MAX = math.inf
MIN = -math.inf


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
    moves = []
    current_board_state = np.zeros((9, 9), dtype=int)
    exists = False
    while True:
        if os.path.exists("jonilo.go"):
            exists = True
        if exists:
            with open("move_file", "r") as fp:
                # Get last non-empty line from file
                line = ""
                for next_line in fp.readlines():
                    if next_line.isspace():
                        break
                    else:
                        line = next_line
                        current_position = line.split()
                        if current_position[0] == "jonilo":
                            current_board_state[int(current_position[1])][int(current_position[2])] = PLAYER0_MARKER
                        else:
                            current_board_state[int(current_position[1])][int(current_position[2])] = PLAYER1_MARKER
                
                # Tokenize move
                tokens = line.split()

                if len(tokens) > 0:
                    print("tokens: " + str(tokens))
                    # Get board and location
                    board_num = int(tokens[1])
                    location_num = int(tokens[2])

                    # Convert to global coordinates
                    global_location_num = local_to_global([board_num, location_num])

                    # Add move to list
                    moves.append((board_num, location_num))

                    # Write to move file
                    # board location is the last local location that was played
                    write_to_move_file(current_board_state, location_num)

                    # Remove jonilo.go file
                    os.remove("jonilo.go")
                    exists = False
                    # time.sleep(2)

                else:
                    # open first_four_moves and get the last move
                    with open("first_four_moves", "r") as fp:
                        # Get last non-empty line from file
                        line = ""
                        for next_line in fp.readlines():
                            if next_line.isspace():
                                break
                            else:
                                line = next_line
                                current_position = line.split()
                                if current_position[0] == "jonilo":
                                    current_board_state[int(current_position[1])][int(current_position[2])] = PLAYER0_MARKER
                                else:
                                    current_board_state[int(current_position[1])][int(current_position[2])] = PLAYER1_MARKER

                        # Tokenize move
                        tokens = line.split()

                        if len(tokens) > 0:
                            print("tokens from first_four_moves: " + str(tokens))
                            # Get board and location
                            board_num = int(tokens[1])
                            location_num = int(tokens[2])

                            # Convert to global coordinates
                            global_location_num = local_to_global([board_num, location_num])

                            # Add move to list
                            moves.append((board_num, location_num))

                            # Write to move file
                            # board location is the last local location that was played
                            write_to_move_file(current_board_state, location_num)

                            # Remove jonilo.go file
                            os.remove("jonilo.go")
                            exists = False
                            # time.sleep(2)


def minimax_decision(board, local_board_to_play):

    # get all valid moves
    valid_moves_list = valid_moves(board, local_board_to_play, False)

    bestValue = 0
    bestCoord = [0, 0]
    for i in range(3):
        for j in range(3):

            state = board

            if state[i][j] == NO_MARKER:

                state[i][j] = PLAYER0_MARKER
                value = minimax_value(0, state, False, MIN, MAX, local_board_to_play)

                if value > bestValue and (i, j) in valid_moves_list:
                    bestCoord = [i,j]
                    bestValue = value

                state[i][j] = NO_MARKER
    return bestCoord


def minimax_value(depth, board, isMaxPlayer, alpha, beta, local_board_to_play):
    if(valid_moves_3x3_global(board, local_board_to_play, isMaxPlayer) == []):
        score = util_function(board)
    else:
        score = eval_function(board, isMaxPlayer)
    # score = 0	
    # Implement DRAW and BAD_MOVE cases

    print("score: " + str(score))

    if depth == 3:
        return score

    if isMaxPlayer:
        V = MIN
        for i in range(3):
            for j in range(3):
                # Create a temporary board so main board does not have issues
                state = board

                if state[i][j] == NO_MARKER:
                    # PLAYER0_MARKER most likely needs to change
                    state[i][j] = PLAYER0_MARKER
                    val = minimax_value(depth + 1, state, False, alpha, beta, local_board_to_play)
                    V = max(V, val)

                    alpha = max(alpha, V)
                    state[i][j] = NO_MARKER

                    # This might need to be in the first loop and not second
                    if beta <= alpha:
                        break

        # print(V)
        return V

    else:
        V = MAX
        for i in range(3):
            for j in range(3):
                # Create a temporary board so main board does not have issues
                state = board

                if state[i][j] == NO_MARKER:
                    # PLAYER1_MARKER most likely needs to change
                    state[i][j] = PLAYER1_MARKER
                    val = minimax_value(depth + 1, state, True, alpha, beta, local_board_to_play)
                    V = min(V, val)

                    beta = min(beta, V)
                    state[i][j] = NO_MARKER

                    if beta <= alpha:
                        break
        # print(V)
        return V


def util_function(board):
    # This is going to be a function that given a terminal global board returns the number of points won by the
    # current player
    # Check if there is a check for global board if not we have to implement it ourselves
    return


def eval_function(board, local_board_to_play):
    # Add heuristic function here
    # Evaluates non-terminal global board configs
    # Must coincide (be equal to) util_function on terminal global board configs
    # This also might have to change
    all_valid_moves = valid_moves_3x3_global(board, local_board_to_play, False)
    # convert to local coordinates
    



def write_to_move_file(board, local_board_to_play):
    move_file = open("move_file", "w")
    # We will want to change this to whatever move that ab pruning finds the most beneficial
    best_coord = minimax_decision(board, local_board_to_play)
    move_file.write("jonilo" + " " + str(best_coord[0]) + " " + str(best_coord[1]) + "\n")
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
