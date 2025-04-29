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