import math
import os

from core_gameplay import NO_MARKER, PLAYER0_MARKER, PLAYER1_MARKER, local_to_global, check_3x3_win

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
                    write_to_move_file(location_num)

                    # Remove jonilo.go file
                    os.remove("jonilo.go")
                    exists = False

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
                            write_to_move_file(location_num)

                            # Remove jonilo.go file
                            os.remove("jonilo.go")
                            exists = False


def minimax(depth, board, isMaxPlayer, boardResults, alpha, beta):
    score = eval_function(board)
    # Implement DRAW and BAD_MOVE cases

    if depth == 3:
        return boardResults[board]

    if isMaxPlayer:
        V = MIN
        for i in range(3):
            for j in range(3):
                if board[i][j] == NO_MARKER:
                    # PLAYER0_MARKER most likely needs to change
                    board[i][j] = PLAYER0_MARKER
                    val = minimax(depth + 1, board, False, boardResults, alpha, beta)
                    V = max(V, val)

                    alpha = max(alpha, V)
                    board[i][j] = NO_MARKER

                    # This might need to be in the first loop and not second
                    if beta <= alpha:
                        break
        return V

    else:
        V = MAX
        for i in range(3):
            for j in range(3):
                if board[i][j] == NO_MARKER:
                    # PLAYER1_MARKER most likely needs to change
                    board[i][j] = PLAYER1_MARKER
                    val = minimax(depth + 1, board, True, boardResults, alpha, beta)
                    V = min(V, val)

                    beta = min(beta, V)
                    board[i][j] = NO_MARKER

                    if beta <= alpha:
                        break
        return V


def util_function(currPlayerState, otherPlayerState):
    # This is going to be a function that given a terminal global board returns the number of points won by the
    # current player
    return currPlayerState - otherPlayerState


def eval_function(board):
    # Evaluates non-terminal global board configs
    # Must coincide (be equal to) util_function on terminal global board configs
    return check_3x3_win(board)


def write_to_move_file(board):
    move_file = open("move_file", "w")
    # We will want to change this to whatever move that ab pruning finds the most beneficial
    move_file.write("jonilo" + " " + str(board) + " " + str(2) + "\n")
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
