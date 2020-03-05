import random
from functools import reduce

MINIMUM_INITIAL_PILE_SIZE = 1


class nim:
    def __init__(self, piles=3, objects=20, seed=None):
        random.seed(seed)
        assert objects >= piles*MINIMUM_INITIAL_PILE_SIZE
        objects -= piles*MINIMUM_INITIAL_PILE_SIZE
        self.piles = [MINIMUM_INITIAL_PILE_SIZE for _ in range(piles)]
        self.current_player = 0
        self.done = False
        for _ in range(objects):
            self.piles[random.randint(0, piles-1)] += 1

    def possible_actions(self):
        return reduce(lambda a, b: a+b, [[(i, j) for j in range(1, pile+1)] for i, pile in enumerate(self.piles)])

    def act(self, action):
        pile, objects_taken = action
        assert self.piles[pile] >= objects_taken
        self.piles[pile] -= objects_taken
        self.current_player = 1-self.current_player
        self.done = reduce(lambda a, b: a+b, self.piles) == 0
        return self.done

    def copy(self):
        _copy = nim(0, 0, 0)
        _copy.piles = self.piles.copy()
        _copy.current_player = self.current_player
        _copy.done = self.done
        return _copy
# game = nim(3, 24, 0)
# print(game.piles)
# print(game.possible_actions())
