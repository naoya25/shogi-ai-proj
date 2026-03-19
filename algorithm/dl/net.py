import torch
import torch.nn as nn
import torch.nn.functional as F


class ShogiNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(43, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)

        # policy head
        self.policy_conv = nn.Conv2d(64, 2, 1)
        self.policy_fc = nn.Linear(2 * 9 * 9, 2187)

        # value head
        self.value_conv = nn.Conv2d(64, 1, 1)
        self.value_fc1 = nn.Linear(9 * 9, 64)
        self.value_fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # policy
        p = F.relu(self.policy_conv(x))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)

        # value
        v = F.relu(self.value_conv(x))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))

        return p, v
