import random

from algorithm.search.minmax import minimax_stack

from .evaluation import evaluate


def search(board, depth):
    """
    depth: 探索深さ
    depthまで探索し、minmax法で最善手を探索(DFS)
    """

    best_score, best_moves = minimax_stack(board, depth, evaluate)

    print(f"info score cp {best_score}")
    return random.choice(best_moves)
