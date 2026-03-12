def minimax(board, depth, max_depth, maximizing, evaluate):
    if depth == max_depth or board.is_game_over():
        return evaluate(board), []

    moves = list(board.legal_moves)

    best_value = -float("inf") if maximizing else float("inf")

    best_moves = []

    for move in moves:
        board.push(move)

        val, _ = minimax(board, depth + 1, max_depth, not maximizing, evaluate)

        board.pop()

        if maximizing:
            if val > best_value:
                best_value = val
                best_moves = [move]
            elif val == best_value:
                best_moves.append(move)

        else:
            if val < best_value:
                best_value = val
                best_moves = [move]
            elif val == best_value:
                best_moves.append(move)

    return best_value, best_moves
