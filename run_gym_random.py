import gym
from gym import wrappers, logger

from pong_game import PongGame
from gym_agents import RandomAgent
from time import sleep

if __name__ == '__main__':
    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = PongGame()
    env.seed(0)
    agent1 = RandomAgent(env.action_space)
    agent2 = RandomAgent(env.action_space)

    episode_count = 1
    reward = 0
    done = False
    print(env.action_space.n)

    for i in range(episode_count):
        ob = env.reset()
        while True:
            action1 = agent1.act(ob, reward, done)
            action2 = agent2.act(ob, reward, done)
            ob, reward, done, _ = env.step(action1, a2=action2)
            if done:
                break
            env.render()

    # Close the env and write monitor result info to disk
    env.close()
