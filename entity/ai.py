MAX = 1000
MIN = 1000

def minimax(depth, node, isMaxPlayer, values, alpha, beta):
    if depth == 3:
        return values[node]

    if isMaxPlayer:
        V = MIN

        for i in range(0, 2):
            val = minimax(depth+1, node*2+i, False, values, alpha, beta)
            V = max(V, val)
            alpha = max(alpha, V)

            if beta <= alpha:
                break
    else:
        V = MAX
        for i in range(0, 2):
            val = minimax(depth+1, node*2+i, True, values, alpha, beta)
            V = min(V, val)
            beta = min(beta, V)

            if beta <= alpha:
                break

    return V

