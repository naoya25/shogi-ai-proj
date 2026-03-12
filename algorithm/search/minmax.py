def minimax_stack(board, max_depth, evaluate):

    stack = [
        {
            "board": board.copy(),
            "depth": 0,
            "maximizing": not board.turn,
            "state": 0,
        }
    ]

    values = {}
    best_moves = {}

    while stack:
        node = stack.pop()

        b = node["board"]
        d = node["depth"]
        maximizing = node["maximizing"]
        state = node["state"]

        key = b.zobrist_hash()

        if state == 0:
            if d == max_depth or b.is_game_over():
                values[key] = evaluate(b)
                continue

            stack.append(
                {
                    "board": b,
                    "depth": d,
                    "maximizing": maximizing,
                    "state": 1,
                }
            )

            moves = list(b.legal_moves)

            for move in moves:
                child = b.copy()
                child.push(move)

                stack.append(
                    {
                        "board": child,
                        "depth": d + 1,
                        "maximizing": not maximizing,
                        "state": 0,
                    }
                )

        else:
            moves = list(b.legal_moves)

            child_values = []
            child_moves = []

            for move in moves:
                child = b.copy()
                child.push(move)

                child_values.append(values[child.zobrist_hash()])
                child_moves.append(move)

            if maximizing:
                best_value = max(child_values)
            else:
                best_value = min(child_values)

            best_indices = [i for i, v in enumerate(child_values) if v == best_value]

            values[key] = best_value
            best_moves[key] = [child_moves[i] for i in best_indices]

    root_hash = board.zobrist_hash()
    return values[root_hash], best_moves.get(root_hash)
