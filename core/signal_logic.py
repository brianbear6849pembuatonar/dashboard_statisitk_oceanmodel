import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
#pengaturan lowpass filter
class SignalProcessor:
    @staticmethod
    def moving_average(series, window_hours, sr_min):
        window_size = int((window_hours * 60) / sr_min)
        return series.rolling(window=max(1, window_size), center=True, min_periods=1).mean()

    @staticmethod
    def butterworth_lowpass(series, cutoff_hours, sr_min, order=4):
        # Clean NaNs
        y = series.interpolate().fillna(method='bfill').fillna(method='ffill').values
        nyquist = 0.5 * (1 / (sr_min * 60))
        cutoff_hz = 1 / (cutoff_hours * 3600)
        wn = cutoff_hz / nyquist
        
        if wn >= 1: return series.values
        b, a = butter(order, wn, btype='low')
        return filtfilt(b, a, y)

    @staticmethod
    def resample_averaging(df, time_col, y_col, hours):
        return df.set_index(time_col)[y_col].resample(f"{hours}H").mean().reset_index()
