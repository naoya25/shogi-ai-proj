import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random

import cshogi

from ai.evaluation import evaluate, evaluate_negamax
from algorithm.search.minmax import minimax
from algorithm.search.negamax import negamax

DEPTH = 3
N_GAMES = 50


# 実装方法は違うが、アルゴリズム的には同じことをしているので互角になるはず
def test_minmax_vs_negamax_play():

    wins = 0
    losses = 0
    draws = 0

    for i in range(N_GAMES):
        print(f"================= game {i + 1} of {N_GAMES} =================\n")

        board = cshogi.Board()

        # 先後をランダム
        first_player = random.choice([cshogi.BLACK, cshogi.WHITE])

        turn_count = 0

        while not board.is_game_over():
            turn_count += 1

            if board.turn == first_player:
                score, moves = minimax(board, 0, DEPTH, not board.turn, evaluate)
                move = random.choice(moves)
            else:
                score, moves = negamax(board, 0, DEPTH, evaluate_negamax)
                move = random.choice(list(board.legal_moves))

            board.push(move)

        # 終局処理
        if board.is_draw():
            draws += 1
            continue

        # 勝者判定（手番側が負け）
        if board.turn == cshogi.BLACK:
            winner = cshogi.WHITE
        else:
            winner = cshogi.BLACK

        if winner == first_player:
            wins += 1
        else:
            losses += 1

        print("games:", N_GAMES)
        print("minimax win:", wins)
        print("negamax win:", losses)
        print("draw:", draws)
        print("win rate:", wins / (wins + losses))

    print("games:", N_GAMES)
    print("minimax win:", wins)
    print("negamax win:", losses)
    print("draw:", draws)
    print("win rate:", wins / (wins + losses))
