import pandas as pd


class PDLogger:
    def __init__(self, name: str) -> None:
        self.data = []
        self.current_run = []
        self.name = name
        self.run_num = 0
        self.log_num = 0

    def log_path_length(self, length: int) -> None:
        self.current_run.append(length)
        self.log_num += 1

    def inc_run(self) -> None:
        self.data.append(self.current_run)
        self.run_num += 1
        self.log_num = 0
        self.current_run = []

    def save_to_file(self, winner: str):
        format_data = pd.DataFrame(self.data)
        format_data.to_csv(self.name + '-winner-' + winner + '.csv', index=False)

    def add_run_stats(self, extra_data: pd.DataFrame):
        extra_data.to_csv(self.name + '.csv', mode='a', header=True)
