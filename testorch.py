import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.l1 = nn.Linear(1, 3)
        self.l2 = nn.Linear(3, 3)
        self.l3 = nn.Linear(3, 2)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x

def update_dqn(state, action, next_state, reward):
    ## 各変数をtensorに変換
    state = torch.FloatTensor([state])
    action = torch.LongTensor([action]) # indexとして使うのでLong型
    next_state = torch.FloatTensor([next_state])

    ## Q値の算出
    q_now = dqn(state).gather(-1, action) # 今の状態のQ値
    max_q_next = dqn(next_state).max(-1)[0].detach() # 状態移行後の最大のQ値
    gamma = 0.9
    q_target = reward + gamma * max_q_next # 目標のQ値

    # DQNパラメータ更新
    optimizer.zero_grad()
    loss = criterion(q_now, q_target) # 今のQ値と目標のQ値で誤差を取る
    loss.backward()
    optimizer.step()
    
    return loss.item() # lossの確認のために返す

############################################################################

def update_dqn(state, action, next_state, reward):
    ## 各変数をtensorに変換
    state = torch.FloatTensor([state])
    action = torch.LongTensor([action]) # indexとして使うのでLong型
    next_state = torch.FloatTensor([next_state])

    ## Q値の算出
    q_now = dqn(state).gather(-1, action) # 今の状態のQ値
    max_q_next = dqn(next_state).max(-1)[0].detach() # 状態移行後の最大のQ値
    gamma = 0.9
    q_target = reward + gamma * max_q_next # 目標のQ値

    # DQNパラメータ更新
    optimizer.zero_grad()
    loss = criterion(q_now, q_target) # 今のQ値と目標のQ値で誤差を取る
    loss.backward()
    optimizer.step()
    
    return loss.item() # lossの確認のために返す
#
dqn = DQN()
optimizer = torch.optim.SGD(dqn.parameters(), lr=0.01)
criterion = nn.MSELoss()

state=20.1
action=0
next_state=25.3
reward=0.1
state = torch.FloatTensor([state])
action = torch.LongTensor([action]) # indexとして使うのでLong型
next_state = torch.FloatTensor([next_state])
#
q_now = dqn(state).gather(-1, action) # 今の状態のQ値
max_q_next = dqn(next_state).max(-1)[0].detach() # 状態移行後の最大のQ値
gamma = 0.9
q_target = reward + gamma * max_q_next # 目標のQ値
#
optimizer.zero_grad()
loss = criterion(q_now, q_target) # 今のQ値と目標のQ値で誤差を取る
loss.backward()
optimizer.step()
#
print(loss.item())