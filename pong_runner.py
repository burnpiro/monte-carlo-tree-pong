from mcts import Mcts
from pong.pong_game import PongGame
from pong.gym_agents import RandomAgent, AggressiveAgent, GreedyAgent
from time import sleep, time
from pong.gym_agents import *
from pong.monitor import PongMonitor

possible_opponents = {
    1: RandomAgent,
    2: GreedyAgent,
    3: AggressiveAgent,
    4: LazyAgent
}

print("Welcome in Pong")
selected_opponent,  = input(
    "Select opponent for MCTS (1 - Random, 2 - Safe, 3 - Aggressive, 4 - Lazy): ").split()

game = PongGame()
game = PongMonitor(game, ".", force=True)
game.reset()

opponent = possible_opponents[int(selected_opponent)]()
mcts_agent = GreedyAgent()

tree = Mcts(game, simulation_agent=mcts_agent)

count = 0

while not game.done:
    count = count + 1
    start = time()
    tree.run(10)
    stop = time()
    ob = game._get_obs()
    # if ob is not None:
    #     game.ale.saveScreenPNG('images/' + str(count) + '-state.png')
    #     print(count, end=" ")
    #     for i, val in enumerate(ob):
    #         print(val, end=" ")
    #     print("")
    print("total time: ", stop - start)
    action1 = tree.predict()
    action2 = opponent.act(ob, player=1)

    game.act(action1)
    tree.move_root(action1)
    game.act(action2)
    tree.move_root(action2)

    game.render()
