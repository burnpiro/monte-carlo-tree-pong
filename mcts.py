from __future__ import annotations
import math
import random
from typing import List, Set, Dict, Tuple
from nim import Action, Nim


class MctsTree:
    def __init__(self, possible_actions: List[Action], game_state: Nim) -> None:
        self.children = {}
        self.possible_actions: Set[Action] = set(possible_actions)
        self._is_leaf: bool = True
        self._simulations: int = 0
        self._wins: int = 0
        self._state: Nim = game_state.copy()

    def is_leaf(self) -> bool:
        return self._state.done or bool(self.possible_actions - self.children.keys())

    def choose_child_node(self, exploration_parameter: int):
        exploration_values: Dict[int] = {}

        for action in self.possible_actions:
            child_node = self.children[action]
            win_rate = child_node._wins / child_node._simulations
            exploration = math.sqrt(
                math.log(self._simulations) / child_node._simulations)
            exploration_values[child_node] = win_rate + exploration

        return max(exploration_values, key=lambda x: exploration_values[x])

    def expand(self) -> MctsTree:
        if self._state.done:
            # dont expand terminating leaves
            return self
        action: Action = (self.possible_actions - self.children.keys()).pop()
        new_state: Nim = self._state.copy()
        new_state.act(action)
        new_node: MctsTree = MctsTree(new_state.possible_actions(), new_state)
        self.children[action] = new_node
        return new_node

    def simulate(self) -> int:
        game = self._state.copy()
        done = game.done
        while not done:
            actions = game.possible_actions()
            action = random.choice(actions)
            done = game.act(action)
        return game.current_player


class Mcts:
    def __init__(self, game: Nim) -> None:
        self.game: Nim = game.copy()
        self.root: MctsTree = MctsTree(game.possible_actions(), game)
        self._exploration_parameter: int = 1.41

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
                node._wins += 1
            node._simulations += 1

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
        return max(self.root.children, key=lambda x: self.root.children[x]._simulations)

    def move_root(self, action) -> None:
        if action in self.root.children:
            self.root = self.root.children[action]
        else:
            new_state = self.root._state.copy()
            new_state.act(action)
            self.root = MctsTree(new_state.possible_actions(), new_state)
