import random

from algorithm.search.alpha_beta import alpha_beta

from .evaluation import evaluate_negamax


def search(board):
    """
    depth: 探索深さ
    depthまで探索し、minmax法で最善手を探索(DFS)
    """

    best_score, best_moves = alpha_beta(
        board,
        0,
        4,
        -float("inf"),
        float("inf"),
        evaluate_negamax,
    )

    print(f"info score cp {best_score}")
    return random.choice(best_moves)
