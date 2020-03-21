from __future__ import annotations
from typing import Union, Tuple, List, Type
import random
import gym
from gym.spaces import Discrete, Box
import numpy as np
import atari_py
from pong.gym_agents import *
from gym.envs.atari.atari_env import AtariEnv

ACTION = int
POSSIBLE_PLAYERS = Type[Union[GreedyAgent, AggressiveAgent, RandomAgent, None]]


class PongGame(AtariEnv):
    def __init__(self, second_player: POSSIBLE_PLAYERS = None):
        super().__init__()
        self._seconf_player_class: POSSIBLE_PLAYERS = second_player
        self._is_multiplayer = second_player is not None
        self._action_set = self.ale.getMinimalActionSet()
        self._action_set2 = [x + 18 for x in self._action_set]
        self.winning_player = -1
        self.current_player = 1
        self.done = False
        self._player2_bot: POSSIBLE_PLAYERS = second_player(self.action_space,
                                                            player=2) if not self._is_multiplayer else None

    def step(self, a1: ACTION, a2: Union[ACTION, None] = None):
        action1 = self._action_set[a1]
        a2 = a2 or a1
        action2 = self._action_set2[a2]
        reward = self.ale.act2(action1, action2)
        ob = self._get_obs()
        return ob, reward

    # Do not make this static because MCTS requires it
    def possible_actions(self) -> List[ACTION]:
        return [FIRE, DOWN, UP]

    def act(self, action1: ACTION, action2: Union[ACTION, None] = None) -> bool:
        if action2 is None and self._player2_bot is not None:
            action2 = self._player2_bot.act(self._get_obs())

        ob, reward = self.step(action1, action2)

        # reward could be only -1, 0 and 1 (-1 and 1 means there is a point scored by one of the sides)
        if reward != 0:
            self.winning_player = 1 if reward == 1 else 2
            self.done = True

        return reward != 0

    def act_random(self) -> bool:
        action1 = random.choice(self.possible_actions())
        action2 = None
        if self._player2_bot is not None:
            action2 = self._player2_bot.act(self._get_obs())

        self.done = self.act(action1, action2)
        return self.done

    def reset(self):
        super().reset()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.soft_reset()

    def copy(self) -> PongGame:
        _new_game = PongGame(self._seconf_player_class)
        _new_game.restore_full_state(self.clone_full_state())

        return _new_game
