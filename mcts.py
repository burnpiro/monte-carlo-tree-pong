from __future__ import annotations
from typing import Union, Tuple, List
import math
import random
from typing import List, Set, Dict, Tuple
from nim.nim import Nim, ACTION as NIM_ACTION
from pong.pong_game import PongGame, ACTION as PONG_ACTION
from pong.monitor import PongMonitor
from pd_logger import PDLogger

EXPLORATION_PARAMETER = 1.41

AVAILABLE_ACTION = Union[NIM_ACTION, PONG_ACTION]
GAME = Union[Nim, PongGame, PongMonitor]


class MctsTree:
    def __init__(self, possible_actions: List[AVAILABLE_ACTION], game: GAME, prev_player: int = None) -> None:
        self.children = {}
        self.possible_actions: Set[AVAILABLE_ACTION] = set(possible_actions)
        self._is_leaf: bool = True
        self.simulations: int = 0
        self.wins: int = 0
        self._state = game.get_state()
        self._terminating = game.done
        self.current_player = game.current_player
        self.prev_player = prev_player
        self.game = game

    def is_leaf(self) -> bool:
        return self._terminating or bool(self.possible_actions - self.children.keys())

    def choose_child_node(self, exploration_parameter: float):
        exploration_values: Dict[int] = {}

        for action in self.possible_actions:
            child_node = self.children[action]
            win_rate = child_node.wins / child_node.simulations
            exploration = exploration_parameter * math.sqrt(
                math.log(self.simulations) / child_node.simulations)
            exploration_values[child_node] = win_rate + exploration

        return max(exploration_values, key=lambda x: exploration_values[x])

    def expand(self) -> MctsTree:
        if self._terminating:
            # dont expand terminating leaves
            return None
        action = (self.possible_actions - self.children.keys()).pop()
        self.restore_game_state()
        prev_player = self.game.current_player
        self.game.act(action)
        new_node: MctsTree = MctsTree(
            self.game.possible_actions(), self.game, prev_player)
        self.children[action] = new_node
        return new_node

    def simulate(self, simulation_agent=None, max_simulation_steps=300) -> int:
        self.restore_game_state()
        score = self._terminating
        step = 0
        while not score and step < max_simulation_steps:
            if simulation_agent:
                action = simulation_agent.act(
                    self.game._get_obs(), player=self.game.current_player)
                score = self.game.act(action)
            else:
                score = self.game.act_random()
            step += 1
        return score

    def restore_game_state(self):
        self.game.set_state(self._state, self._terminating,
                            self.current_player)

    def __repr__(self):
        return str(self._state) + '%d/%d' % (self.wins, self.simulations)


class Mcts:
    def __init__(self, game: GAME, simulation_agent=None, max_simulation_steps=300, logger: PDLogger=None) -> None:
        self.game: GAME = game.copy()
        self.root: MctsTree = MctsTree(
            game.possible_actions(), self.game)
        self._exploration_parameter: float = EXPLORATION_PARAMETER
        self.simulation_agent = simulation_agent
        self.max_simulation_steps = max_simulation_steps
        self.logger = logger

    def selection(self) -> Tuple[List[MctsTree], MctsTree]:
        path = [self.root]
        potential_leaf = self.root
        while not potential_leaf.is_leaf():
            potential_leaf = potential_leaf.choose_child_node(
                self._exploration_parameter)
            path.append(potential_leaf)

        return path, potential_leaf

    def backpropagation(self, path: List[MctsTree], score: int) -> None:
        for node in path:
            if (node.prev_player == 0 and score == 1) or (node.prev_player == 1 and score == -1):
                node.wins += 1
            node.simulations += 1

    def step(self) -> int:
        path, leaf = self.selection()
        new_node = leaf.expand()
        if new_node:  # if leaf is not terminating add expanded node to path
            path.append(new_node)
        else:
            new_node = leaf  # run simulation on terminating node instead
        score = new_node.simulate(
            simulation_agent=self.simulation_agent,
            max_simulation_steps=self.max_simulation_steps
        )
        self.backpropagation(path, score)
        return len(path)

    def run(self, steps: int, verbose: bool = False) -> None:
        max_length = 0
        for _ in range(steps):
            current_state = self.step()
            max_length = current_state if current_state > max_length else max_length
            if self.logger is not None:
                self.logger.log_path_length(current_state)

        if verbose:
            print(max_length)

        if self.logger is not None:
            self.logger.inc_run()
        # self.root.restore_game_state()

    def predict(self):
        return max(self.root.children, key=lambda x: self.root.children[x].simulations)

    def move_root(self, action) -> None:
        if action in self.root.children:
            self.root = self.root.children[action]
        else:
            self.root.restore_game_state()
            self.game.act(action)
            self.root = MctsTree(self.game.possible_actions(), self.game)
