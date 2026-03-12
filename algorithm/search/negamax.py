
def negamax(board, depth, max_depth, evaluate):
    """
    評価値は、手番側が+、相手が-に統一
    """
    if depth == max_depth or board.is_game_over():
        return evaluate(board), []

    moves = list(board.legal_moves)

    best_value = -float("inf")
    best_moves = []

    for move in moves:
        board.push(move)

        val, _ = negamax(board, depth + 1, max_depth, evaluate)
        val = -val

        board.pop()

        if val > best_value:
            best_value = val
            best_moves = [move]
        elif val == best_value:
            best_moves.append(move)

    return best_value, best_moves
