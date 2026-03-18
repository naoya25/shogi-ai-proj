import cshogi
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

from algorithm.dl.mcts import mcts, move_to_index
from algorithm.dl.net import ShogiNet
from utils.board_to_tensor import board_to_tensor

net = ShogiNet()

board = cshogi.Board()

move, visit_counts = mcts(board, net, simulations=200)

print(cshogi.move_to_usi(move))


MAX_MOVES = 300


def self_play(net, simulations=200):
    board = cshogi.Board()

    game_data = []
    move_count = 0
    history = {}

    while not board.is_game_over():
        # 最大手数制限
        if move_count >= MAX_MOVES:
            break

        # MCTSで探索
        move, visit_counts = mcts(board, net, simulations)

        # policy教師作成
        policy = np.zeros(2187)

        total = sum(visit_counts.values())

        for m, v in visit_counts.items():
            idx = move_to_index(m)
            policy[idx] = v / total

        # state保存
        state = board_to_tensor(board)

        game_data.append((state, policy, board.turn))

        board.push(move)

        move_count += 1

        sfen = board.sfen().rsplit(" ", 1)[0]
        history[sfen] = history.get(sfen, 0) + 1

        # 千日手判定
        if history[sfen] >= 4:
            break

    # 勝敗
    if move_count >= MAX_MOVES or board.is_draw():
        result = cshogi.DRAW
    else:
        if board.turn == cshogi.BLACK:
            result = cshogi.WHITE_WIN
        else:
            result = cshogi.BLACK_WIN

    dataset = []

    for state, policy, turn in game_data:
        if result == cshogi.DRAW:
            value = 0
        elif result == cshogi.BLACK_WIN:
            value = 1 if turn == cshogi.BLACK else -1
        elif result == cshogi.WHITE_WIN:
            value = 1 if turn == cshogi.WHITE else -1

        dataset.append((state, policy, value))

    return dataset


class ShogiDataset(Dataset):
    def __init__(self, data):
        self.states = []
        self.policies = []
        self.values = []

        for s, p, v in data:
            self.states.append(s)
            self.policies.append(p)
            self.values.append(v)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        state = torch.tensor(self.states[idx]).float()
        policy = torch.tensor(self.policies[idx]).float()
        value = torch.tensor(self.values[idx]).float()

        return state, policy, value


def compute_loss(pred_p, pred_v, target_p, target_v):
    # policy
    log_prob = F.log_softmax(pred_p, dim=1)

    policy_loss = -(target_p * log_prob).sum(dim=1).mean()

    # value
    value_loss = F.mse_loss(pred_v.squeeze(), target_v)

    return policy_loss + value_loss


def train_network(net, dataset, epochs=5, batch_size=64):
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)

    for _ in range(epochs):
        for state, policy, value in loader:
            pred_p, pred_v = net(state)

            loss = compute_loss(pred_p, pred_v, policy, value)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


net = ShogiNet()

memory = []

for iteration in range(1000):
    print("self play")

    for _ in range(10):
        game_data = self_play(net)
        memory.extend(game_data)

    dataset = ShogiDataset(memory)

    print("training")

    train_network(net, dataset)

    # モデル保存
    torch.save(net.state_dict(), f"models/model_{iteration}.pt")
