import math

MAX = math.inf
MIN = -math.inf


def minimax(depth, node, isMaxPlayer, values, alpha, beta):
    # For the future lets think of what node is and depending on it, we will expand accordingly
    if depth == 3:
        return values[node]

    if isMaxPlayer:
        V = MIN
        for i in range(0, 2):
            # To elaborate if node is like a listNode we would do node.child or something
            val = minimax(depth + 1, node * 2 + i, False, values, alpha, beta)
            V = max(V, val)
            alpha = max(alpha, V)

            if beta <= alpha:
                break
    else:
        V = MAX
        for i in range(0, 2):
            val = minimax(depth + 1, node * 2 + i, True, values, alpha, beta)
            V = min(V, val)
            beta = min(beta, V)

            if beta <= alpha:
                break

    return V
