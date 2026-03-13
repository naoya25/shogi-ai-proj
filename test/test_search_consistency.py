import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random

import cshogi

from ai.evaluation import evaluate, evaluate_negamax
from algorithm.search.alpha_beta import alpha_beta
from algorithm.search.minimax import minimax

random.seed(42)

DEPTH = 3
N_TESTS = 100


def random_position(board, plies=20):
    """ランダム局面生成"""

    board.reset()

    for _ in range(plies):
        moves = list(board.legal_moves)

        if not moves:
            break

        board.push(random.choice(moves))

# アルゴリズムの整合性をテストする
def test_search_consistency():
    board = cshogi.Board()

    for i in range(N_TESTS):
        random_position(board)

        score1, move1 = minimax(board, 0, DEPTH, not board.turn, evaluate)

        score2, move2 = alpha_beta(
            board,
            0,
            DEPTH,
            -float("inf"),
            float("inf"),
            evaluate_negamax,
        )

        if score1 != score2 or move1 != move2:
            print("Mismatch found!")
            print("SFEN:", board.sfen())
            print("Minimax:", score1, move1)
            print("AlphaBeta:", score2, move2)

            assert False
