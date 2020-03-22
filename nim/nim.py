from __future__ import annotations
import random
from typing import List, Tuple
from functools import reduce

MINIMUM_INITIAL_PILE_SIZE = 1

ACTION = Tuple[int, int]


class Nim:
    def __init__(self, piles: int = 3, objects: int = 20, seed: int or None = None) -> None:
        random.seed(seed)
        assert objects >= piles * MINIMUM_INITIAL_PILE_SIZE
        objects -= piles * MINIMUM_INITIAL_PILE_SIZE
        self.piles: List[int] = [
            MINIMUM_INITIAL_PILE_SIZE for _ in range(piles)]
        self.current_player: int = 0
        self.done: bool = False

        # distribute objects randomly into piles
        for _ in range(objects):
            self.piles[random.randint(0, piles - 1)] += 1

    # Generate list of actions base on piles size and number
    def possible_actions(self) -> List[ACTION]:
        return reduce(lambda acc, list_of_actions: acc + list_of_actions,
                      [[(pile_idx, j) for j in range(1, pile + 1)] for pile_idx, pile in enumerate(self.piles)])

    def act(self, action: ACTION) -> bool:
        pile, objects_taken = action

        # Make sure that pile size has enough objects to take from
        assert self.piles[pile] >= objects_taken
        self.piles[pile] -= objects_taken

        # Count number of objects left and check if game is done
        self.done = reduce(lambda acc, pile_size: acc +
                           pile_size, self.piles) == 0
        if not self.done:
            self.current_player = 1 - self.current_player
            return 0
        self.done = 1 if self.current_player == 0 else -1
        return self.done

    def act_random(self) -> bool:
        actions = self.possible_actions()
        action = random.choice(actions)
        return self.act(action)

    def copy(self) -> Nim:
        _copy = Nim(0, 0, 0)
        _copy.piles = self.piles[:]
        _copy.current_player = self.current_player
        _copy.done = self.done
        return _copy

    def get_state(self):
        return self.piles.copy()

    def set_state(self, state, done, current_player):
        self.done = done
        self.current_player = current_player
        self.piles = state.copy()
