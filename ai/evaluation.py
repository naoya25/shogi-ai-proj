import cshogi

from utils.const import MATE_SCORE

PIECE_VALUE = {
    cshogi.PAWN: 100,
    cshogi.LANCE: 300,
    cshogi.KNIGHT: 300,
    cshogi.SILVER: 400,
    cshogi.GOLD: 500,
    cshogi.BISHOP: 800,
    cshogi.ROOK: 1000,
    cshogi.PROM_PAWN: 500,
    cshogi.PROM_LANCE: 500,
    cshogi.PROM_KNIGHT: 500,
    cshogi.PROM_SILVER: 500,
    cshogi.PROM_BISHOP: 900,
    cshogi.PROM_ROOK: 1100,
}


def evaluate(board):
    """
    先手: +, 後手: -
    駒得を計算するのみ
    """
    # 詰み判定
    if board.is_game_over():
        if board.turn == cshogi.BLACK:
            return -MATE_SCORE
        else:
            return MATE_SCORE

    score = 0

    # 持ち駒
    for piece in board.pieces:
        if piece == 0:
            continue

        piece_type = piece & 15
        value = PIECE_VALUE.get(piece_type, 0)

        if piece < 16:
            score += value
        else:
            score -= value

    # 持ち駒
    hand_black, hand_white = board.pieces_in_hand

    for hp in range(7):
        piece_type = cshogi.hand_piece_to_piece_type(hp)
        value = PIECE_VALUE[piece_type]

        score += hand_black[hp] * value
        score -= hand_white[hp] * value

    return score


def evaluate_negamax(board):
    """
    手番側が+、相手が-
    """
    score = evaluate(board)

    if board.turn == cshogi.BLACK:
        return score
    else:
        return -score
