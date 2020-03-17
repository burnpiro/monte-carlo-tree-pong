class RandomAgent():
    def __init__(self, action_space, **kwargs):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()


class GreedyAgent():
    pallet_height = 5

    def __init__(self, action_space, player=1, **kwargs):
        self.action_space = action_space
        self.player = player

    def act(self, observation, reward, done):
        if observation is not None and observation[54] != 0:
            pos = observation[60] if self.player == 1 else observation[59]
            pos += GreedyAgent.pallet_height
            ball_pos = observation[54]
            if pos-GreedyAgent.pallet_height*0.6 > ball_pos:
                return 2
            if pos+GreedyAgent.pallet_height*0.6 < ball_pos:
                return 3
            return 0
        else:
            return 0
