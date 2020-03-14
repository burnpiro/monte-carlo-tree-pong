import gym
from gym import wrappers, logger

from pong_game import PongGame


class RandomAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample(), self.action_space.sample()


if __name__ == '__main__':
    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = PongGame()
    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    print(env.action_space.n)

    for i in range(episode_count):
        ob = env.reset()
        while True:
            action1, action2 = agent.act(ob, reward, done)
            # print(action)
            ob, reward, done, _ = env.step(action1, a2=action2)
            # print(reward)
            # print(ob.size)
            if done:
                break
            env.render()

    # Close the env and write monitor result info to disk
    env.close()
