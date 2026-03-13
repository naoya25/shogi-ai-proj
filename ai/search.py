from algorithm.search.alpha_beta import alpha_beta

from .evaluation import evaluate_negamax


def search(board):
    best_score, best_move = alpha_beta(
        board, 0, 3, -float("inf"), float("inf"), evaluate_negamax
    )

    print(f"info score cp {best_score}")
    return best_move
