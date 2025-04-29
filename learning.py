import matplotlib.pyplot as plt

NUM_EPISODES = 1200
NUM_STEPS = 5

log = [] # 結果のプロット用

for episode in range(NUM_EPISODES):
    env = Dispenser(0)
    total_reward = 0 # 1エピソードでの報酬の合計を保持する

    for s in range(NUM_STEPS):
        ## 現在の状態を確認
        state = env.state
        ## 行動を決める
        action = decide_action(state, episode)
        ## 決めた行動に従いステップを進める。次の状態、報酬を得る
        next_state, reward = env.step(action)
        ## DQNを更新
        loss = update_dqn(state, action, next_state, reward)
        total_reward += reward

    log.append([total_reward, loss])

## 結果表示
r, l = np.array(log).T
fig = plt.figure(figsize=(11,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_xlabel("Episode")
ax1.set_ylabel("Loss")
ax1.set_yscale("log")
ax2.set_xlabel("Episode")
ax2.set_ylabel("Total reward")
ax1.plot(l)
ax2.plot(r)
plt.show()