import numpy as np

EPS_START = 0.9
EPS_END = 0.0
EPS_DECAY = 200

def decide_action(state, episode):
    state = torch.FloatTensor([state]) # 状態を1次元tensorに変換
    ## ε-グリーディー法
    eps = EPS_END + (EPS_START - EPS_END) * np.exp(-episode / EPS_DECAY)
    if eps <= np.random.uniform(0, 1):
        with torch.no_grad():
            action = dqn(state).max(-1)[1] # Q値が最大のindexが得られる
            action = action.item() # 0次元tensorを通常の数値に変換
    else:
        num_actions = len(dqn(state)) # action数取得
        action = np.random.choice(np.arange(num_actions)) # ランダム行動
    return action