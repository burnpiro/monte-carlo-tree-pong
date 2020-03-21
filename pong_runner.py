from mcts import Mcts
from pong.pong_game import PongGame
from pong.gym_agents import RandomAgent, AggressiveAgent, GreedyAgent
from time import sleep

possible_opponents = {
    1: RandomAgent,
    2: GreedyAgent,
    3: AggressiveAgent
}

print("Welcome in Pong")
selected_opponent,  = input("Select opponent for MCTS (1 - Random, 2 - Safe, 3 - Aggressive): ").split()

opponent = possible_opponents[int(selected_opponent)]
game = PongGame(opponent)
tree = Mcts(game)
tree.run(1)

game.reset()
while not game.done:
    if game.done:
        print("You won!")
        exit()

    tree.run(10)
    action = tree.predict()
    game.act(action)
    tree.move_root(action)
    game.render()
    sleep(0.03)

    print("Enemy move: "+str(action))

print("You lost!")
