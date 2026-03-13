import math
import random

from algorithm.search.alpha_beta import alpha_beta
from utils.const import MATE_SCORE


def root_search(board, depth, evaluate):
    moves_score = []

    for move in board.legal_moves:
        board.push(move)
        score, _ = alpha_beta(
            board, 0, depth - 1, -float("inf"), float("inf"), evaluate
        )
        score = -score

        moves_score.append((move, score))
        board.pop()

    moves_score.sort(key=lambda x: x[1], reverse=True)

    return select_move_with_softmax(moves_score)


def select_move_with_softmax(moves_score, top_n=5, temperature=1.0):
    # まず詰み手があればそれを確定
    for move, score in moves_score:
        if abs(score) >= MATE_SCORE:
            return score, move  # 確定

    # 上位top_n手を選択
    moves_score.sort(key=lambda x: x[1], reverse=True)
    top_moves = moves_score[:top_n]

    # スコアを正規化
    scores = [s / 100 for _, s in top_moves]

    # 最大値を引いて安定化
    max_score = max(scores)
    exp_scores = [math.exp((s - max_score) / temperature) for s in scores]
    total = sum(exp_scores)
    probs = [e / total for e in exp_scores]

    # 確率に従って1手選択
    chosen_index = random.choices(range(len(top_moves)), weights=probs, k=1)[0]
    chosen_move, chosen_score = top_moves[chosen_index]

    return chosen_score, chosen_move
