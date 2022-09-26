import math

MAX = math.inf
MIN = -math.inf


def minimax(depth, board, isMaxPlayer, boardResults, alpha, beta):
    if depth == 3:
        return boardResults[board]

    if isMaxPlayer:
        V = MIN
        for i in range(0, 2):
            val = minimax(depth + 1, board * 2 + i, False, boardResults, alpha, beta)
            V = max(V, val)
            alpha = max(alpha, V)

            if beta <= alpha:
                break
    else:
        V = MAX
        for i in range(0, 2):
            val = minimax(depth + 1, board * 2 + i, True, boardResults, alpha, beta)
            V = min(V, val)
            beta = min(beta, V)

            if beta <= alpha:
                break

    return V


def util_function(currPlayerState, otherPlayerState):
    # This is going to be a function that given a terminal global board returns the number of points won by the
    # current player
    return currPlayerState - otherPlayerState


def eval_function():
    # Evaluates non-terminal global board configs
    # Must coincide (be equal to) util_function on terminal global board configs
    return


if __name__ == "__main__":
    minimax(0, 0, False, 0, 0, 0)
