import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import random

import cshogi

from algorithm.dl.move_to_index import move_to_index


def _random_position(board: cshogi.Board, plies: int = 30) -> None:
    board.reset()
    for _ in range(plies):
        moves = list(board.legal_moves)
        if not moves:
            return
        board.push(random.choice(moves))
        if board.is_game_over():
            board.reset()


def test_move_to_index_is_unique_over_legal_moves_random_positions():
    """
    重要性が高い性質:
    同一局面の合法手集合上で move_to_index が衝突しないこと。
    """
    random.seed(0)
    board = cshogi.Board()

    for _ in range(200):
        _random_position(board, plies=40)

        seen = {}
        for mv in board.legal_moves:
            idx = move_to_index(mv, board.turn)
            assert 0 <= idx < 2187
            if idx in seen and seen[idx] != mv:
                a = cshogi.move_to_usi(seen[idx])
                b = cshogi.move_to_usi(mv)
                raise AssertionError(
                    f"index collision: idx={idx} a={a} b={b} sfen={board.sfen()}"
                )
            seen[idx] = mv


def test_drop_moves_are_in_drop_bucket_when_present():
    """
    打ちの move_type は 20..26 を使う想定なので、
    打ち手が存在する局面が見つかったらその性質を確認する。
    """
    random.seed(1)
    board = cshogi.Board()

    found_drop = False
    for _ in range(400):
        _random_position(board, plies=60)
        for mv in board.legal_moves:
            if cshogi.move_from(mv) >= 81:
                found_drop = True
                idx = move_to_index(mv, board.turn)
                assert idx % 27 >= 20
        if found_drop:
            break

    assert found_drop, (
        "no drop move found in sampled random positions; increase sampling if needed"
    )


def test_promotion_flag_affects_move_type_when_present():
    """
    成り手が存在する局面が見つかったら、promoteフラグで move_type の偶奇が変わることを確認。
    (move_type = base_dir*2 + promote を想定)
    """
    random.seed(2)
    board = cshogi.Board()

    found_promo = False
    for _ in range(800):
        _random_position(board, plies=80)
        for mv in board.legal_moves:
            if cshogi.move_is_promotion(mv):
                found_promo = True
                idx = move_to_index(mv, board.turn)
                assert idx % 2 == 1
                assert (idx % 27) < 20  # 通常手の範囲
        if found_promo:
            break

    assert found_promo, (
        "no promotion move found in sampled random positions; increase sampling if needed"
    )
