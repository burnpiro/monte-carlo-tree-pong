from mcts import Mcts
from pong.pong_game import PongGame
import pandas as pd
from pong.gym_agents import RandomAgent, AggressiveAgent, GreedyAgent
from time import sleep, time
from pong.gym_agents import *
from pd_logger import PDLogger
from datetime import datetime
from pong.monitor import PongMonitor

possible_opponents = {
    1: RandomAgent,
    2: GreedyAgent,
    3: AggressiveAgent,
    4: LazyAgent
}

opponent_names = {
    1: 'RandomAgent',
    2: 'GreedyAgent',
    3: 'AggressiveAgent',
    4: 'LazyAgent'
}

print("Welcome in Pong")

playouts = []

for method in ['greedy', 'random']:
    for agent in [2, 3]:
        for run in range(5, 80, 5):
            playouts.append({
                'runs': run,
                'agent': agent,
                'method': method
            })

for playout in playouts:
    print('Playing pong with {} runs, using {} method, against {} opponent'.format(playout['runs'], playout['method'], opponent_names[
        playout['agent']]))
    game = PongGame()
    # game = PongMonitor(game, ".", force=True)
    game.reset()

    pong_logger = PDLogger('./logs-2/pong-' + playout['method'] + '-' + str(playout['runs']) + '-against-' + opponent_names[
        playout['agent']] + '_' + datetime.now().strftime("%Y%m%d-%H%M%S"))
    opponent = possible_opponents[agent]()
    mcts_agent = GreedyAgent()

    tree = None
    if playout['method'] == 'greedy':
        tree = Mcts(game, simulation_agent=mcts_agent, logger=pong_logger)

    if playout['method'] == 'random':
        tree = Mcts(game, logger=pong_logger)

    count = 0

    while not game.done:
        count = count + 1
        start = time()
        tree.run(playout['runs'], verbose=True)
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

    pong_logger.save_to_file('mcts' if game.get_winner() == 0 else 'bot')
    # print(game.get_winner())
    # pong_logger.add_run_stats(pd.DataFrame({
    #     'winning_player': [game.get_winner()],
    #     'opponent': opponent_names[playout['agent']],
    #     'runs': [playout['runs']],
    #     'method': [playout['method']]
    # }))
    game.reset()
    game.close()
