# アルゴリズムの計算速度を計測するテスト
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random
import time

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


def generate_positions(n):
    """同じ局面セットを作る"""
    board = cshogi.Board()
    positions = []

    for _ in range(n):
        random_position(board)
        positions.append(board.sfen())

    return positions


def run_minimax(positions):
    start = time.perf_counter()

    for sfen in positions:
        board = cshogi.Board(sfen)
        minimax(board, 0, DEPTH, not board.turn, evaluate)

    end = time.perf_counter()

    return end - start


def run_alphabeta(positions):
    start = time.perf_counter()

    for sfen in positions:
        board = cshogi.Board(sfen)
        alpha_beta(
            board,
            0,
            DEPTH,
            -float("inf"),
            float("inf"),
            evaluate_negamax,
        )

    end = time.perf_counter()

    return end - start


def test_search_speed():
    positions = generate_positions(N_TESTS)

    # t_minimax = run_minimax(positions)
    t_alphabeta = run_alphabeta(positions)

    print("\n=== Search Speed Test ===")
    # print(f"Minimax:   {t_minimax:.4f} sec")
    # print(f"Minimax avg:   {t_minimax / N_TESTS:.6f} sec/pos")
    print(f"AlphaBeta: {t_alphabeta :.4f} sec")
    print(f"AlphaBeta avg: {t_alphabeta / N_TESTS:.6f} sec/pos")

    # αβの方が遅いのは普通あり得ないのでチェック
    # assert t_alphabeta < t_minimax
