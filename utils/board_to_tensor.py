import cshogi
import numpy as np


# cshogi.Board を学習用Tensorに変換
def board_to_tensor(board):
    # 42ch: 盤面(14*2) + 持ち駒(7*2)
    # +1ch: 手番 (BLACKなら1, WHITEなら0)
    planes = np.zeros((43, 9, 9), dtype=np.float32)

    # --- 盤面 ---
    for sq in range(81):
        piece = board.piece(sq)

        if piece == 0:
            continue

        piece_type = piece & 15
        color = 0 if piece < 16 else 1  # BLACK=0 WHITE=1

        channel = piece_type - 1

        if color == 1:
            channel += 14

        y = sq // 9
        x = sq % 9

        planes[channel][y][x] = 1.0

    # --- 持ち駒 ---
    hand_offset = 28

    hand_black, hand_white = board.pieces_in_hand

    for hp in range(7):
        piece_type = cshogi.hand_piece_to_piece_type(hp)

        # BLACK
        planes[hand_offset + hp][:][:] = hand_black[hp]

        # WHITE
        planes[hand_offset + 7 + hp][:][:] = hand_white[hp]

    # --- 手番 ---
    planes[42][:][:] = 1.0 if board.turn == cshogi.BLACK else 0.0

    return planes
