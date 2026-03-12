import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random

import cshogi

from ai.evaluation import evaluate
from algorithm.search.minmax import minimax_stack

DEPTH_A = 2
DEPTH_B = 3
N_GAMES = 50


def test_minmax_vs_minmax_play():

    wins = 0
    losses = 0
    draws = 0

    for i in range(N_GAMES):
        print(f"================= game {i + 1} of {N_GAMES} =================\n")

        board = cshogi.Board()

        # minimax側の先後をランダム
        first_player = random.choice([cshogi.BLACK, cshogi.WHITE])

        turn_count = 0

        while not board.is_game_over():
            turn_count += 1

            if board.turn == first_player:
                score, moves = minimax_stack(board, DEPTH_A, evaluate)
                move = random.choice(moves)
            else:
                score, moves = minimax_stack(board, DEPTH_B, evaluate)
                move = random.choice(moves)


            board.push(move)

            if turn_count % 30 == 0:
                print(f"turn {turn_count} of game {i + 1}")

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
    print("minimax depth2 win:", wins)
    print("minimax depth3 win:", losses)
    print("draw:", draws)
    print("win rate:", wins / (wins + losses))
