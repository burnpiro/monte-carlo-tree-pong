from mcts import Mcts
from nim import Nim

game = Nim(3, 20)
tree = Mcts(game)
tree.run(1)

print("Hello in Nim")


while not game.done:
    print(game.piles)
    move = input("Your move: ").split()
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
