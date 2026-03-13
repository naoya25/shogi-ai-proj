def alpha_beta(board, depth, max_depth, alpha, beta, evaluate):
    """
    αβ探索
    最善手は1手のみを返す
    """

    if depth == max_depth or board.is_game_over():
        return evaluate(board), None

    best_value = -float("inf")
    best_move = None

    for move in board.legal_moves:
        board.push(move)

        val, _ = alpha_beta(board, depth + 1, max_depth, -beta, -alpha, evaluate)
        val = -val

        board.pop()

        if val > best_value:
            best_value = val
            best_move = move

        alpha = max(alpha, val)

        if alpha >= beta:
            break

    return best_value, best_move
