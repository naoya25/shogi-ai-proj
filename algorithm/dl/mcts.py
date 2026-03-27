import math

import numpy as np
import torch

from algorithm.dl.move_to_index import move_to_index
from utils.board_to_tensor import board_to_tensor


class Node:
    def __init__(self, board, parent=None, move=None):

        self.board = board
        self.parent = parent
        self.move = move

        self.children = {}

        self.policy = 0
        self.win = 0
        self.n = 0


def evaluate(board, net):
    x = board_to_tensor(board)
    x = torch.tensor(x).unsqueeze(0).float()

    with torch.no_grad():
        p, v = net(x)

    p = torch.softmax(p, dim=1)

    return p[0], v.item()


def expand(node, net):
    policy, value = evaluate(node.board, net)

    for move in node.board.legal_moves:
        next_board = node.board.copy()
        next_board.push(move)

        child = Node(next_board, node, move)

        move_id = move_to_index(move, node.board.turn)

        child.policy = policy[move_id].item()

        node.children[move] = child

    return value


def puct(parent, child, c=1.4):
    if child.n == 0:
        Q = 0
    else:
        Q = -child.win / child.n  # child視点 → parent視点に変換

    U = c * child.policy * math.sqrt(parent.n) / (1 + child.n)

    return Q + U


def select(node):
    return max(node.children.values(), key=lambda c: puct(node, c))


def backpropagate(node, value):
    while node:
        node.n += 1
        node.win += value

        value = -value

        node = node.parent


def mcts(
    board,
    net,
    simulations=200,
    add_dirichlet_noise=False,
    dirichlet_alpha=0.3,
    dirichlet_eps=0.25,
    temperature=0.0,
    sample_move=False,
):
    root = Node(board)

    expand(root, net)

    # ルートにDirichletノイズを付与（自己対局用）
    if add_dirichlet_noise and root.children:
        children = list(root.children.values())
        priors = np.array([c.policy for c in children], dtype=np.float64)
        if priors.sum() <= 0:
            priors = np.ones_like(priors) / len(priors)
        noise = np.random.dirichlet([dirichlet_alpha] * len(children))
        mixed = (1.0 - dirichlet_eps) * priors + dirichlet_eps * noise
        for c, p in zip(children, mixed):
            c.policy = float(p)

    for _ in range(simulations):
        node = root

        # Selection
        while node.children:
            node = select(node)

        # Expansion
        value = expand(node, net)

        # Backpropagation
        backpropagate(node, value)

    # 訪問回数取得
    visit_counts = {child.move: child.n for child in root.children.values()}

    # 手の選択: 自己対局用には visit_counts に基づくサンプリングを使えるようにする
    if sample_move and temperature > 0 and visit_counts:
        moves = list(visit_counts.keys())
        counts = np.array([visit_counts[m] for m in moves], dtype=np.float64)
        if counts.sum() <= 0:
            counts = np.ones_like(counts)
        if temperature != 1.0:
            counts = counts ** (1.0 / temperature)
        probs = counts / counts.sum()
        move = np.random.choice(moves, p=probs)
    else:
        move = max(root.children.values(), key=lambda c: c.n).move

    return move, visit_counts
