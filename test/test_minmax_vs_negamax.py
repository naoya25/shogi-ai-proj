import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random
import time
from datetime import datetime

import cshogi
from cshogi import KIF

from ai.evaluation import evaluate, evaluate_negamax
from algorithm.search.minmax import minimax
from algorithm.search.negamax import negamax

DEPTH = 3
N_GAMES = 50
MAX_MOVES = 300

random.seed(42)


# 実装方法は違うが、アルゴリズム的には同じことをしているので互角になるはず
def test_minmax_vs_negamax_play():
    wins = 0
    losses = 0
    draws = 0

    for i in range(N_GAMES):
        print(f"================= game {i + 1} of {N_GAMES} =================\n")

        board = cshogi.Board()
        moves_record = []

        # 先後を交互に
        first_player = cshogi.BLACK if i % 2 == 0 else cshogi.WHITE

        turn_count = 0
        start = time.time()

        while not board.is_game_over() and turn_count < MAX_MOVES:
            turn_count += 1

            if board.turn == first_player:
                score, moves = minimax(board, 0, DEPTH, not board.turn, evaluate)
                move = random.choice(moves)
            else:
                score, moves = negamax(board, 0, DEPTH, evaluate_negamax)
                move = random.choice(moves)

            board.push(move)
            moves_record.append(move)

        # 手数制限
        if turn_count >= MAX_MOVES:
            draws += 1
            result = "draw"

        elif board.is_draw():
            draws += 1
            result = "draw"

        else:
            if board.turn == cshogi.BLACK:
                winner = cshogi.WHITE
            else:
                winner = cshogi.BLACK

            if winner == first_player:
                wins += 1
            else:
                losses += 1

            result = "resign"

        print("games:", N_GAMES)
        print("minimax win:", wins)
        print("negamax win:", losses)
        print("draw:", draws)
        print("win rate:", wins / (wins + losses))
        elapsed_seconds = int(time.time() - start)
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        print(f"time: {hours:02d}:{minutes:02d}:{seconds:02d}")

        today_str = datetime.now().strftime("%Y%m%d")
        kif_filename = f"kif/test_minmax_vs_negamax_{today_str}_{i}.kif"
        exporter = KIF.Exporter(kif_filename)
        exporter.header(
            ["Minimax", "Negamax"]
            if first_player == cshogi.BLACK
            else ["Negamax", "Minimax"]
        )
        for move in moves_record:
            exporter.move(move)
        exporter.end(result)

    print("games:", N_GAMES)
    print("minimax win:", wins)
    print("negamax win:", losses)
    print("draw:", draws)
    print("win rate:", wins / (wins + losses))
