import math

import cshogi
import torch

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


def move_to_index(move):
    from_sq = cshogi.move_from(move)
    to_sq = cshogi.move_to(move)

    # --- 打ち駒 ---
    if from_sq >= 81:
        drop_type = from_sq - 81  # 0〜6

        move_type = 20 + drop_type

        idx = to_sq * 27 + move_type

        assert 0 <= idx < 2187

        return idx

    # --- 通常手 ---
    fx = from_sq % 9
    fy = from_sq // 9

    tx = to_sq % 9
    ty = to_sq // 9

    dx = tx - fx
    dy = ty - fy

    dx = max(-1, min(1, dx))
    dy = max(-1, min(1, dy))

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

    move_type = direction_map.get((dx, dy), 0)

    idx = from_sq * 27 + move_type

    assert 0 <= idx < 2187

    return idx


def expand(node, net):
    policy, value = evaluate(node.board, net)

    for move in node.board.legal_moves:
        next_board = node.board.copy()
        next_board.push(move)

        child = Node(next_board, node, move)

        move_id = move_to_index(move)

        child.policy = policy[move_id].item()

        node.children[move] = child

    return value


def puct(parent, child, c=1.4):
    if child.n == 0:
        Q = 0
    else:
        Q = child.win / child.n

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


def mcts(board, net, simulations=200):
    root = Node(board)

    expand(root, net)

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

    best_child = max(root.children.values(), key=lambda c: c.n)

    return best_child.move, visit_counts
