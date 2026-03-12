import random

from algorithm.search.negamax import negamax

from .evaluation import evaluate_negamax


def search(board, depth):
    """
    depth: 探索深さ
    depthまで探索し、minmax法で最善手を探索(DFS)
    """

    best_score, best_moves = negamax(board, 0, depth, evaluate_negamax)

    print(f"info score cp {best_score}")
    return random.choice(best_moves)
