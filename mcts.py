from __future__ import annotations
from typing import Union, Tuple, List
import math
import random
from typing import List, Set, Dict, Tuple
from nim.nim import Nim, ACTION as NIM_ACTION
from pong.pong_game import PongGame, ACTION as PONG_ACTION

EXPLORATION_PARAMETER = 1.41

AVAILABLE_ACTION = Union[NIM_ACTION, PONG_ACTION]
GAME = Union[Nim, PongGame]


class MctsTree:
    def __init__(self, possible_actions: List[AVAILABLE_ACTION],
                 game_state: GAME) -> None:
        self.children = {}
        self.possible_actions: Set[AVAILABLE_ACTION] = set(possible_actions)
        self._is_leaf: bool = True
        self.simulations: int = 0
        self.wins: int = 0
        self._state: GAME = game_state.copy()

    def is_leaf(self) -> bool:
        return self._state.done or bool(self.possible_actions - self.children.keys())

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
        if self._state.done:
            # dont expand terminating leaves
            return self
        action = (self.possible_actions - self.children.keys()).pop()
        new_state: GAME = self._state.copy()
        new_state.act(action)
        new_node: MctsTree = MctsTree(new_state.possible_actions(), new_state)
        self.children[action] = new_node
        return new_node

    def simulate(self) -> int:
        game = self._state.copy()
        done = game.done
        while not done:
            done = game.act_random()
        return game.winning_player


class Mcts:
    def __init__(self, game: GAME) -> None:
        self.game: GAME = game.copy()
        self.root: MctsTree = MctsTree(game.possible_actions(), game)
        self._exploration_parameter: float = EXPLORATION_PARAMETER

    def selection(self) -> Tuple[List[MctsTree], MctsTree]:
        path = [self.root]
        potential_leaf = self.root
        while not potential_leaf.is_leaf():
            potential_leaf = potential_leaf.choose_child_node(
                self._exploration_parameter)
            path.append(potential_leaf)

        return path, potential_leaf

    def backpropagation(self, path: List[MctsTree], winning_player: int) -> None:
        for node in path:
            if node._state.current_player == winning_player:
                node.wins += 1
            node.simulations += 1

    def step(self) -> None:
        path, leaf = self.selection()
        new_node = leaf.expand()
        path.append(new_node)
        winning_player = new_node.simulate()
        self.backpropagation(path, winning_player)

    def run(self, steps: int) -> None:
        for _ in range(steps):
            self.step()

    def predict(self):
        return max(self.root.children, key=lambda x: self.root.children[x].simulations)

    def move_root(self, action) -> None:
        if action in self.root.children:
            self.root = self.root.children[action]
        else:
            new_state = self.root._state.copy()
            new_state.act(action)
            self.root = MctsTree(new_state.possible_actions(), new_state)
