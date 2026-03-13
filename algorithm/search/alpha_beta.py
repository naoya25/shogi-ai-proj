def alpha_beta(board, depth, max_depth, alpha, beta, evaluate):
    """
    Negamax 形式の αβ探索。

    `evaluate(board)` は「手番側が+、相手が-」の評価値を返す前提。
    """
    if depth == max_depth or board.is_game_over():
        return evaluate(board), []

    moves = list(board.legal_moves)

    best_value = -float("inf")
    best_moves = []

    for move in moves:
        board.push(move)

        val, _ = alpha_beta(board, depth + 1, max_depth, -beta, -alpha, evaluate)
        val = -val

        board.pop()

        if val > best_value:
            best_value = val
            best_moves = [move]
        elif val == best_value:
            best_moves.append(move)

        alpha = max(alpha, val)

        if alpha >= beta:
            break  # βカット

    return best_value, best_moves
