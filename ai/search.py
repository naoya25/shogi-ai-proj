import torch

from algorithm.dl.mcts import mcts
from algorithm.dl.net import ShogiNet

# モデル読み込み
net = ShogiNet()
net.load_state_dict(torch.load("models/model_90.pt"))
net.eval()


def search(board):
    # best_score, best_move = alpha_beta(
    #     board, 0, 3, -float("inf"), float("inf"), evaluate_negamax
    # )

    # print(f"info score cp {best_score}")
    # return best_move

    move, _ = mcts(board, net)
    return move
