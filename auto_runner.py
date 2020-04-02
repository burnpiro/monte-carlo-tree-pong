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

for method in ['greedy']:
    for agent in [3]:
        for run in [5, 35, 60]:
            for i in range(0, 15):
                playouts.append({
                    'runs': run,
                    'agent': agent,
                    'method': method,
                    'skip_actions': False,
                    'exploration_parameter': 1.41
                })

for playout in playouts:
    print('Playing pong with {} runs, using {} method, against {} opponent'.format(playout['runs'], playout['method'],
                                                                                   opponent_names[
                                                                                       playout['agent']]))
    game = PongGame()
    filename = './logss/' + playout['method'] + '-no-skip-1.41/pong-' + playout['method'] + '-' + str(
        playout['runs']) + '-against-' + opponent_names[
                   playout['agent']] + '_' + datetime.now().strftime("%Y%m%d-%H%M%S")
    game = PongMonitor(game, filename, force=False)
    game.reset()

    pong_logger = PDLogger(filename)
    opponent = possible_opponents[agent]()
    mcts_agent = GreedyAgent()

    tree = None
    if playout['method'] == 'greedy':
        tree = Mcts(game, simulation_agent=mcts_agent, logger=pong_logger, skip_actions=playout['skip_actions'],
                    exploration_parameter=playout['exploration_parameter'])

    if playout['method'] == 'random':
        tree = Mcts(game, logger=pong_logger, skip_actions=playout['skip_actions'],
                    exploration_parameter=playout['exploration_parameter'])

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
        # print("total time: ", stop - start)
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
