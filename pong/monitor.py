from gym.wrappers import Monitor
from .pong_game import PongGame, ACTION
from typing import Union, Tuple, List, Type


class PongMonitor(Monitor):
    def __init__(self, pong_env: PongGame, directory, video_callable=None, force=False, resume=False, write_upon_reset=False, uid=None, mode=None):
        super().__init__(pong_env, directory, video_callable=video_callable, force=force,
                         resume=resume, write_upon_reset=write_upon_reset, uid=uid, mode=mode)

    def step(self, a1: ACTION, a2: Union[ACTION, None] = None):
        ob, reward = self.env.step(a1, a2)
        self._after_step(ob, reward, self.env.done, None)

    def act(self, action: ACTION) -> int:
        score = self.env.act(action)
        self._after_step(None, score, self.env.done, None)

    def _get_obs(self):
        return self.env._get_obs()
