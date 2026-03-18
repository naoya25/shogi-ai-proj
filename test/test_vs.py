import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import random
import time
from datetime import datetime

import cshogi
import torch
from cshogi import KIF

from ai.evaluation import evaluate_negamax
from algorithm.dl.mcts import mcts
from algorithm.dl.net import ShogiNet
from algorithm.search.root_search import root_search

N_GAMES = 1000  # 対局数
MAX_MOVES = 300  # 手数制限 超えたら引き分け

random.seed(42)

net = ShogiNet()
net.load_state_dict(torch.load("models/model_90.pt"))
net.eval()

PLAYERS = [
    (
        "AlphaBeta + 駒得",
        lambda board: root_search(board, 3, evaluate_negamax),
    ),
    (
        "MCTS",
        lambda board: mcts(board, net),
    ),
]


def test_vs_play():
    wins = 0
    losses = 0
    draws = 0

    for i in range(N_GAMES):
        print(f"\n================= game {i + 1} of {N_GAMES} =================\n")

        board = cshogi.Board()
        moves_record = []

        # 先後を交互に
        first_player = cshogi.BLACK if i % 2 == 0 else cshogi.WHITE

        turn_count = 0
        start = time.time()

        while not board.is_game_over() and turn_count < MAX_MOVES:
            turn_count += 1

            if board.turn == first_player:
                _, move = PLAYERS[0][1](board)
            else:
                move, _ = PLAYERS[1][1](board)

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
        print(f"{PLAYERS[0][0]} win:", wins)
        print(f"{PLAYERS[1][0]} win:", losses)
        print("draw:", draws)
        print("win rate:", wins / (wins + losses))
        elapsed_seconds = int(time.time() - start)
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        print(f"turn: {turn_count}, time: {hours:02d}:{minutes:02d}:{seconds:02d}")

        # KIF保存
        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        kif_path = Path("kif")
        kif_path.mkdir(exist_ok=True)

        filename = kif_path / f"test_{today_str}_{i}.kif"

        # Exporter 生成
        exporter = KIF.Exporter(str(filename))

        # ヘッダー出力
        exporter.header(
            [PLAYERS[0][0], PLAYERS[1][0]]
            if first_player == cshogi.BLACK
            else [PLAYERS[1][0], PLAYERS[0][0]]
        )
        for move in moves_record:
            exporter.move(move)
        exporter.end(result)
        exporter.close()

    print("============= games:", N_GAMES, "=============")
    print(f"{PLAYERS[0][0]} win:", wins)
    print(f"{PLAYERS[1][0]} win:", losses)
    print("draw:", draws)
    print("win rate:", wins / (wins + losses))
