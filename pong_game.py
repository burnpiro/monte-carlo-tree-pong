import gym
from gym.spaces import Discrete, Box
import numpy as np
import atari_py
from gym.envs.atari.atari_env import AtariEnv


class PongGame(AtariEnv):
    def __init__(self):
        super().__init__()
        self._playerA_actions = [3, 4]
        self._playerB_actions = [21, 22]
        self._action_set = self.ale.getMinimalActionSet()
        self._action_set2 = [x+18 for x in self._action_set]

    def step(self, a1, a2=None):
        action1 = self._action_set[a1]
        a2 = a2 or a1
        action2 = self._action_set2[a2]
        reward = self.ale.act2(action1, action2)
        ob = self._get_obs()
        return ob, reward, self.ale.game_over(), {"ale.lives": self.ale.lives()}

    def reset(self):
        super().reset()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.soft_reset()
