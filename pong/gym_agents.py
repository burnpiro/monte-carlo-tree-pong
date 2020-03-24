from typing import List
import random
# Possible actions are:
# 0: NOOP,
# 1: FIRE,
# 2: UP,
# 3: RIGHT, <- works as down in pong
# 4: LEFT, <- works as up in pong
# 5: DOWN,

NOOP = 0
FIRE = 1
UP = 2
DOWN = 5

RAM_PLAYER_1_POS = 60
RAM_PLAYER_2_POS = 59
RAM_BALL_Y_POS = 54
RAM_BALL_X_POS = 49  # 128 is center, 68 is when hits left agent, 188 when right agent,
# 52 when outside left, 204 when outside right
BOUNCE_COUNT = 17
BALL_IN_THE_WALL = 20  # != 0 means it's in the wall
P_RIGHT_SCORE = 14
P_LEFT_SCORE = 13
ROUND_NUM = 9
BALL_DIRECTION = 18  # 1 means LEFT 0 means RIGHT
# (only applied when ball got hit before that 255 which is also LEFT)
# 0 - no ball, 64 - nothing hit the ball yet (start of the game),
PREVIOUS_HIT_SOURCE = 12
# 128 - wall hit a ball, 192 - player hit a ball. Vales are weird because usually when hit
# it goes from 194 to 192 and from 71 to 64 (71, 70, 69, 68, 67, 66, 65, 54) so better check ranges
# but always starts above the value


def check_if_should_take_action(ob: List[int], player: int = 0):
    """Decides if player should take an action

    Keyword arguments:
    ob -- RAM dump
    player -- 0 (P1 - right) or 1 (P2 - left)
    """
    if player == 0 and ob[RAM_BALL_X_POS] < 128:
        return False
    if player == 1 and ob[RAM_BALL_X_POS] > 128:
        return False
    return True


class RandomAgent:
    def act(self, observation, **kwargs):
        return random.choice([FIRE, DOWN, UP])


class GreedyAgent:
    pallet_height = 5
    center_of_pallet_size = 0.6

    def act(self, observation, player):
        if observation is not None and observation[RAM_BALL_Y_POS] != 0:
            pos = observation[RAM_PLAYER_1_POS] if player == 0 else observation[RAM_PLAYER_2_POS]
            pos += GreedyAgent.pallet_height
            ball_pos = observation[RAM_BALL_Y_POS]
            if pos - GreedyAgent.pallet_height * GreedyAgent.center_of_pallet_size > ball_pos:
                return UP
            if pos + GreedyAgent.pallet_height * GreedyAgent.center_of_pallet_size < ball_pos:
                return DOWN

        return FIRE


class AggressiveAgent:
    pallet_height = 5
    center_of_pallet_size = 0.1
    epsilon = 5  # margin when agent is safe to press FIRE (on edge)

    def act(self, observation, player=0):
        if observation is not None and observation[RAM_BALL_Y_POS] != 0:
            pos = observation[RAM_PLAYER_1_POS] if player == 0 else observation[RAM_PLAYER_2_POS]
            pos += AggressiveAgent.pallet_height
            ball_pos = observation[RAM_BALL_Y_POS]
            if pos - AggressiveAgent.pallet_height * AggressiveAgent.center_of_pallet_size > ball_pos + AggressiveAgent.epsilon:
                return UP
            if pos + AggressiveAgent.pallet_height * AggressiveAgent.center_of_pallet_size < ball_pos - AggressiveAgent.epsilon:
                return DOWN

        return FIRE


class LazyAgent:
    pallet_height = 5
    center_of_pallet_size = 0.1
    epsilon = 5  # margin when agent is safe to press FIRE (on edge)

    def act(self, observation, player=0):
        if observation is not None and observation[RAM_BALL_Y_POS] != 0:
            if not check_if_should_take_action(observation, player):
                return FIRE
            pos = observation[RAM_PLAYER_1_POS] if player == 0 else observation[RAM_PLAYER_2_POS]
            pos += AggressiveAgent.pallet_height
            ball_pos = observation[RAM_BALL_Y_POS]
            if pos - AggressiveAgent.pallet_height * AggressiveAgent.center_of_pallet_size > ball_pos + AggressiveAgent.epsilon:
                return UP
            if pos + AggressiveAgent.pallet_height * AggressiveAgent.center_of_pallet_size < ball_pos - AggressiveAgent.epsilon:
                return DOWN
            return FIRE
        else:
            return FIRE
