def alpha_beta(board, depth, max_depth, alpha, beta, evaluate):
    """
    Negamax 形式の αβ探索。

    `evaluate(board)` は「手番側が+、相手が-」の評価値を返す前提。
    """
    if depth == max_depth or board.is_game_over():
        return evaluate(board), []

    # 注意: αβ探索は root の値自体は正しくても、
    # 探索窓(α/β)によるカットが発生した部分木では、
    # 返る値が境界(upper/lower bound)になり得る。
    # その途中結果で `best_moves` を集計すると、
    # root で「本当は最善でない手」が同値として紛れ込むことがある。
    # root(depth==0) では値確定後に full-window で再評価して最善手集合を作り直す。
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

    # root では「最善手集合」を正確に返す（同値最善手の全列挙）。
    # depth>0 では集合の完全性を保証しない（返り値の `best_value` は正しい）。
    if depth == 0:
        exact_best_moves = []
        for move in moves:
            board.push(move)
            val, _ = alpha_beta(
                board, depth + 1, max_depth, -float("inf"), float("inf"), evaluate
            )
            val = -val
            board.pop()
            if val == best_value:
                exact_best_moves.append(move)
        return best_value, exact_best_moves

    return best_value, best_moves
