from mcts import Mcts
from nim.nim import Nim


print("Hello in Nim")
piles, objects = input(
    "Set game settings (`number of piles` `number of objects`): ").split()

game = Nim(int(piles), int(objects))
tree = Mcts(game, thread_count=8)
tree.run(1)


while not game.done:
    print(game.piles)
    tree.run(1200)
    # move = input("Your move (`pile` `objects`): ").split()
    # action = tuple(int(x) for x in move)
    action = tree.predict()
    print('CPU 0 move: %s' % str(action))
    game.act(action)
    tree.move_root(action)

    if game.done:
        print("You won!")
        exit()

    print(game.piles)

    tree.run(1200)
    action = tree.predict()
    game.act(action)
    tree.move_root(action)

    if tree.root._state != game.piles:
        print('!!!')
        exit()

    print("Enemy move: "+str(action))

print("You lost!")
