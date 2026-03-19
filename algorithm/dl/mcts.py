import math

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
