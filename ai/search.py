import random

from .evaluation import evaluate


def search(board, depth=1):
    """
    1手先の局面を評価し、最善手を探索
    """

    best_moves = []
    best_score = -999999

    for move in board.legal_moves:
        board.push(move)
        score = evaluate(board)
        if board.turn == 0:  # 手番修正
            score = -score

        board.pop()

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    print(f"info score cp {best_score}")
    return random.choice(best_moves)
