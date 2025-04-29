class Dispenser(object):
    def __init__(self, init_state):
        """
        初期のON/OFF状態を設定する
        init_state: 0->電源OFF、1->電源ON
        """
        self.state  = init_state

    def powerbutton(self):
        """
        電源ボタンを押し、ON/OFFを切り替える
        """
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    def step(self, action):
        """
        払出機を操作する
        action: 0->電源ボタンを押す 1->払出ボタンを押す
        状態と報酬が返る
        """
        if action == 0: # 電源ボタンを押した場合
            self.powerbutton() # 電源ON/OFF切り替え
            reward = 0 # 報酬はない
        else:           # 払出ボタンを押した場合
            if self.state == 1:
                reward = 1 # 電源ONのときのみ報酬あり
            else:
                reward = 0
        return self.state, reward