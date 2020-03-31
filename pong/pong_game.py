from __future__ import annotations
from typing import Union, Tuple, List, Type
import random
from itertools import count
import gym
from gym.spaces import Discrete, Box
import numpy as np
import atari_py
from pong.gym_agents import *
from gym.envs.atari.atari_env import AtariEnv
ACTION = int
POSSIBLE_PLAYERS = Type[Union[GreedyAgent, AggressiveAgent, RandomAgent, None]]


class PongGame(AtariEnv):
    _game_count = count(0)

    def __init__(self, second_player: POSSIBLE_PLAYERS = None):

        super().__init__(frameskip=1)
        # self.ale.setInt('frame_skip', 2)
        # self.ale.setFloat('repeat_action_probability', 0.5)
        # self.seed()
        self._game_id = next(self._game_count)
        self._seconf_player_class: POSSIBLE_PLAYERS = second_player
        self._is_multiplayer = second_player is not None
        self._action_set = self.ale.getMinimalActionSet()
        self._action_set2 = [x + 18 for x in self._action_set]
        self.current_player = 0  # 0 (P1) or 1 (P2)
        self.done = False
        self.player_1_action = None
        self._player2_bot: POSSIBLE_PLAYERS = second_player(self.action_space,
                                                            player=2) if self._is_multiplayer is True else None

    def step(self, a1: ACTION, a2: Union[ACTION, None] = None):
        action1 = self._action_set[a1]
        a2 = a2 or a1
        action2 = self._action_set2[a2]
        reward = self.ale.act2(action1, action2)
        ob = self._get_obs()
        return ob, reward

    # Do not make this static because MCTS requires it
    def possible_actions(self, player=None) -> List[ACTION]:
        if player is not None:
            ob = self._get_obs()
            if check_if_should_take_action(ob, player=player):
                return [DOWN, UP]
            return [FIRE]
        return [FIRE, DOWN, UP]

    def act(self, action: ACTION) -> int:
        if self.current_player == 0:
            self.player_1_action = action
            self.current_player = 1
            return False

        ob, reward = self.step(self.player_1_action, action)

        # reward could be only -1, 0 and 1 (-1 and 1 means there is a point scored by one of the sides)
        if reward != 0:
            self.current_player = 0 if reward == 1 else 1
            self.done = True
            return reward

        else:
            self.current_player = 0
            return 0

    def act_random(self) -> bool:
        return self.act(random.choice(self.possible_actions(player=self.current_player)))

    def reset(self):
        super().reset()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.press_select()
        self.ale.soft_reset()
        self.step(FIRE, FIRE)
        while self._get_ram()[RAM_BALL_Y_POS] == 0:
            self.step(FIRE, FIRE)

    def copy(self) -> PongGame:
        _new_game = PongGame(self._seconf_player_class)
        _new_game.restore_full_state(self.clone_full_state())

        return _new_game

    def get_state(self):
        return (self.clone_full_state(), self.player_1_action)

    def set_state(self, state, done, current_player):
        self.done = done
        self.current_player = current_player
        self.restore_full_state(state[0])
        self.player_1_action = state[1]
