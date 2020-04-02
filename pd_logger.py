import pandas as pd
import numpy as np
from typing import Union, Tuple, List


class PDLogger:
    def __init__(self, name: str) -> None:
        self.data = []
        self.current_run = []
        self.name = name
        self.run_num = 0

    def log_paths(self, paths: List[int], time) -> None:
        self.current_run = [np.mean(paths), np.std(paths), np.amax(paths), np.amin(paths), len(paths), time]

    def inc_run(self) -> None:
        self.data.append(self.current_run)
        self.run_num += 1
        self.current_run = []

    def save_to_file(self, winner: str):
        format_data = pd.DataFrame(self.data, columns=['mean', 'std', 'max_length', 'min_length', 'num_of_leafs', 'time'])
        format_data.to_csv(self.name + '-winner-' + winner + '.csv', index=False)

    def add_run_stats(self, extra_data: pd.DataFrame):
        extra_data.to_csv(self.name + '.csv', mode='a', header=True)
