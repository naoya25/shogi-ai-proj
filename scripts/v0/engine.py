"""
合法手からランダムに選ぶAI
"""

import sys
import random
import cshogi

board = cshogi.Board()

while True:
    line = sys.stdin.readline().strip()

    if line == "usi":
        print("id name RandomShogi")
        print("id author YourName")
        print("usiok")
        sys.stdout.flush()

    elif line == "isready":
        print("readyok")
        sys.stdout.flush()

    elif line.startswith("position"):
        parts = line.split()

        board.reset()

        if "moves" in parts:
            i = parts.index("moves")
            moves = parts[i + 1 :]

            for move in moves:
                board.push_usi(move)

    elif line.startswith("go"):
        moves = list(board.legal_moves)

        if len(moves) == 0:
            print("bestmove resign")
        else:
            move = random.choice(moves)
            print("bestmove", cshogi.move_to_usi(move))

        sys.stdout.flush()

    elif line == "quit":
        break
