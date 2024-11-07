import numpy as np


def mean_value(data, name, window=np.blackman(1200), trim=True):
    diff = np.diff(data["time"])
    mean_diff = np.mean(diff)
    if not np.allclose(diff, mean_diff) or mean_diff <= 0:
        msg = "Time should be linearly increasing."
        raise ValueError(msg)
    normalized_window = window / np.sum(window)
    convolution = np.convolve(data[name], normalized_window, mode="same")
    if trim:
        len_window = len(normalized_window) // 2
        convolution[:len_window] = np.nan
        convolution[-len_window:] = np.nan
    return convolution
