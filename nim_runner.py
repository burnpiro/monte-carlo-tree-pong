from mcts import Mcts
from nim import Nim


print("Hello in Nim")
piles, objects = input("Set game settings (`number of piles` `number of objects`): ").split()

game = Nim(int(piles), int(objects))
tree = Mcts(game)
tree.run(1)


while not game.done:
    print(game.piles)
    move = input("Your move (`pile` `objects`): ").split()
    action = tuple(int(x) for x in move)
    game.act(action)
    tree.move_root(action)

    if game.done:
        print("You won!")
        exit()

    print(game.piles)

    tree.run(500)
    action = tree.predict()
    game.act(action)
    tree.move_root(action)

    print("Enemy move: "+str(action))

print("You lost!")
