import cshogi


def move_to_index(move, turn):
    """
    AlphaZero系の定番: 81(to) × 27(action) = 2187

    - 通常手: (8方向 + 桂馬2方向)=10 × (不成/成)=20
    - 打ち: 7

    方向は「to から見た from の位置（= to<-from の逆ベクトル）」を、
    手番視点で正規化して判定する（WHITE番なら180度回転相当）。
    """
    from_sq = cshogi.move_from(move)
    to_sq = cshogi.move_to(move)

    # --- 打ち駒 ---
    if from_sq >= 81:
        drop_type = from_sq - 81  # 0〜6 (歩,香,桂,銀,金,角,飛 の並びを想定)
        move_type = 20 + drop_type  # 20..26
        idx = to_sq * 27 + move_type
        assert 0 <= idx < 2187
        return idx

    # --- 通常手 ---
    fx = from_sq % 9
    fy = from_sq // 9
    tx = to_sq % 9
    ty = to_sq // 9

    # 「to から見た from」(source vector)
    dx = fx - tx
    dy = fy - ty

    # 手番視点で正規化（WHITE番は180度回転）
    if turn == cshogi.WHITE:
        dx = -dx
        dy = -dy

    # 桂馬（手番視点で「前に2、左右に1」）
    # 座標の取り方（x/y軸）が環境で異なっても検出できるよう (1,2)/(2,1) を許容する
    if {abs(dx), abs(dy)} == {1, 2}:
        lateral = dx if abs(dx) == 1 else dy
        base_dir = 8 if lateral < 0 else 9  # 左桂/右桂
    else:
        # 8方向（長手は距離を捨てて方向だけ）
        if dx == 0:
            step = (0, 1 if dy > 0 else -1)
        elif dy == 0:
            step = (1 if dx > 0 else -1, 0)
        else:
            # 斜め（角系）。斜めでない値は通常手として不正（桂馬は上で除外済み）
            if abs(dx) != abs(dy):
                raise ValueError(f"unexpected delta for normal move: dx={dx}, dy={dy}")
            step = (1 if dx > 0 else -1, 1 if dy > 0 else -1)

        direction_map = {
            (0, 1): 0,
            (0, -1): 1,
            (1, 0): 2,
            (-1, 0): 3,
            (1, 1): 4,
            (-1, 1): 5,
            (1, -1): 6,
            (-1, -1): 7,
        }
        base_dir = direction_map[step]  # 0..7

    promote = 1 if cshogi.move_is_promotion(move) else 0
    move_type = base_dir * 2 + promote  # 0..19

    idx = to_sq * 27 + move_type
    assert 0 <= idx < 2187
    return idx
