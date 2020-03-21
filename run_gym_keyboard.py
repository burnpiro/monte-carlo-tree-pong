from gym import wrappers, logger
from pong.pong_game import PongGame

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False


def key_press(key, mod):
    global human_agent_action, human_wants_restart, human_sets_pause
    if key == 0xff0d:
        human_wants_restart = True
    if key == 32:
        human_sets_pause = not human_sets_pause
    a = int(key - ord('0'))
    print(a)
    # 65314 is arrow up and 65316 is arrow down
    if a == 65314:
        a = 2
    if a == 65316:
        a = 3
    if a <= 0 or a >= 6:
        return
    human_agent_action = a


def key_release(key, mod):
    global human_agent_action
    a = int(key - ord('0'))
    # 65314 is arrow up and 65316 is arrow down
    if a == 65314:
        a = 2
    if a == 65316:
        a = 3
    if a <= 0 or a >= 6:
        return
    if human_agent_action == a:
        human_agent_action = 0


print("Press keys (arrow up) (arrow down) to take actions (2 and 3).")
print("No keys pressed is taking action 0 (stay in the same place)")

if __name__ == '__main__':
    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = PongGame()
    outdir = '/tmp/random-agent-results'
    ACTIONS = env.action_space.n

    SKIP_CONTROL = 0  # Use previous control decision SKIP_CONTROL times, that's how you
    # can test what skip is still usable.

    env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    env.render()
    env.unwrapped.viewer.window.on_key_press = key_press
    env.unwrapped.viewer.window.on_key_release = key_release

    episode_count = 100
    reward = 0
    done = False
    print(env.action_space.n)

    for i in range(episode_count):
        ob = env.reset()
        skip = 0
        total_reward = 0
        total_timesteps = 0
        while True:
            if not skip:
                a = human_agent_action
                total_timesteps += 1
                skip = SKIP_CONTROL
            else:
                skip -= 1

            obser, reward, done, info = env.step(a)
            if reward != 0:
                print("reward %0.3f" % reward)
            total_reward += reward
            window_still_open = env.render()
            if not window_still_open:
                break
            if done:
                break
            # time.sleep(0.1)

    # Close the env and write monitor result info to disk
    env.close()
