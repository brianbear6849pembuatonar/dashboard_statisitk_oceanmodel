import pandas as pd
import numpy as np

class DataManager:
    def __init__(self, df: pd.DataFrame, time_col: str):
        self.df = df.copy()
        self.time_col = time_col
        self._standardize()

    def _standardize(self):
        self.df[self.time_col] = pd.to_datetime(self.df[self.time_col])
        self.df = self.df.sort_values(self.time_col).reset_index(drop=True)

    def get_date_range(self):
        return self.df[self.time_col].min().date(), self.df[self.time_col].max().date()

    def filter_by_range(self, start, end, columns):
        mask = (self.df[self.time_col].dt.date >= start) & (self.df[self.time_col].dt.date <= end)
        return self.df.loc[mask, columns].copy()

    def calculate_sampling_rate(self, df):
        if len(df) < 2: return 60.0
        diff = df[self.time_col].diff().dt.total_seconds().median()
        return max(1.0, diff / 60.0) # Dalam menit