from __future__ import annotations
from typing import Union, Tuple, List
import math
import random
from typing import List, Set, Dict, Tuple
from nim.nim import Nim, ACTION as NIM_ACTION
from pong.pong_game import PongGame, ACTION as PONG_ACTION
from multiprocessing.pool import ThreadPool

EXPLORATION_PARAMETER = 1.41

AVAILABLE_ACTION = Union[NIM_ACTION, PONG_ACTION]
GAME = Union[Nim, PongGame]


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
        # self.game = game

    def is_leaf(self) -> bool:
        return self._terminating or bool(len(self.possible_actions) - len(self.children.keys()))

    def unvisited_children(self) -> int:
        if self._terminating:
            return 0
        return len(self.possible_actions) - len(self.children.keys())

    def choose_child_node(self, exploration_parameter: float, forbidden_nodes: set = None):
        exploration_values: Dict[int] = {}

        for action in self.possible_actions:
            child_node = self.children[action]
            if forbidden_nodes and child_node in forbidden_nodes:
                continue
            win_rate = child_node.wins / child_node.simulations
            exploration = exploration_parameter * math.sqrt(
                math.log(self.simulations) / child_node.simulations)
            exploration_values[child_node] = win_rate + exploration

        if exploration_values:
            return max(exploration_values, key=lambda x: exploration_values[x])

        return None

    def expand(self, game) -> MctsTree:
        if self._terminating:
            # dont expand terminating leaves
            return None
        action = (self.possible_actions - self.children.keys()).pop()
        self.restore_game_state(game)
        prev_player = game.current_player
        game.act(action)
        new_node: MctsTree = MctsTree(
            game.possible_actions(), game, prev_player)
        self.children[action] = new_node
        return new_node

    def simulate(self, game, simulation_agent=None, max_simulation_steps=300) -> int:
        self.restore_game_state(game)
        score = self._terminating
        step = 0
        while not score and step < max_simulation_steps:
            if simulation_agent:
                action = simulation_agent.act(
                    game._get_obs(), player=game.current_player)
                score = game.act(action)
            else:
                score = game.act_random()
            step += 1
        return score

    def restore_game_state(self, game):
        game.set_state(self._state, self._terminating,
                       self.current_player)

    def __repr__(self):
        return str(self._state) + '%d/%d' % (self.wins, self.simulations)


class Mcts:
    def __init__(self, game: GAME, thread_count: int = 1, simulation_agent=None, max_simulation_steps=300) -> None:
        self.games: List[GAME] = [game.copy() for _ in range(thread_count)]
        self.thread_count = thread_count
        self.root: MctsTree = MctsTree(
            game.possible_actions(), game)
        self._exploration_parameter: float = EXPLORATION_PARAMETER
        self.thread_pool = ThreadPool(thread_count)
        self.simulation_agent = simulation_agent
        self.max_simulation_steps = max_simulation_steps

    def selection(self) -> Tuple[List[MctsTree], MctsTree]:
        path = [self.root]
        paths = []
        explored_nodes = set()
        targets_count = 0
        current_node = self.root
        while targets_count < self.thread_count and self.root not in explored_nodes:
            while not current_node.is_leaf():
                potential_leaf = current_node.choose_child_node(
                    self._exploration_parameter, explored_nodes)
                if potential_leaf is None:
                    explored_nodes.add(current_node)
                    path.pop()
                    if path:
                        current_node = path[-1]
                        continue
                    else:
                        break

                path.append(potential_leaf)
                current_node = potential_leaf

            if len(path) == 0:
                break

            explored_nodes.add(current_node)
            targets = current_node.unvisited_children()
            targets_count += targets if targets > 0 else 1
            paths.append([node for node in path])
            path.pop()
            if path:
                current_node = path[-1]

        return paths

    def backpropagation(self, paths: List[MctsTree], scores: int) -> None:
        for path, score in zip(paths, scores):
            for node in path:
                if (node.prev_player == 0 and score == 1) or (node.prev_player == 1 and score == -1):
                    node.wins += 1
                elif score == 0:
                    node.wins += 0.5  # przy remisie dodajemy 1/2 dla obu stron
                node.simulations += 1

    def step(self) -> None:
        paths = self.selection()
        paths = self.expand(paths)
        scores = self.simulate(paths)

        self.backpropagation(paths, scores)

    def run(self, steps: int) -> None:
        for _ in range(steps):
            self.step()
        # self.root.restore_game_state()

    def expand(self, paths):
        new_paths = []
        current_path_it = 0
        for _ in range(self.thread_count):
            node = paths[current_path_it][-1]
            while not node.is_leaf():
                current_path_it += 1
                if current_path_it >= len(paths):
                    return new_paths
                node = paths[current_path_it][-1]

            new_node = node.expand(self.games[current_path_it])
            new_path = [n for n in paths[current_path_it]]
            if new_node:
                new_path.append(new_node)
            new_paths.append(new_path)

        return new_paths

    def _run_simulation(self, node, game):
        return node.simulate(game, self.simulation_agent, self.max_simulation_steps)

    def simulate(self, paths):
        results = [self.thread_pool.apply_async(
            self._run_simulation, (path[-1], game)) for (path, game) in zip(paths, self.games)]
        return [r.get() for r in results]

    def predict(self):
        return max(self.root.children, key=lambda x: self.root.children[x].simulations)

    def move_root(self, action) -> None:
        if action in self.root.children:
            self.root = self.root.children[action]
        else:
            game = self.games[0]
            self.root.restore_game_state(game)
            game.act(action)
            self.root = MctsTree(game.possible_actions(), game)
