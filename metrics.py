import numpy as np


def calculate_mean(results):
    return np.mean(results, axis=0)


def calculate_standard_deviation(results):
    return np.std(results, axis=0)


def calculate_minimum(results):
    return np.min(results, axis=0)


def calculate_maximum(results):
    return np.max(results, axis=0)


def calculate_max_height(positions):
    return np.max(positions[:, 2])


def calculate_total_time(times):
    return times[-1]


def calculate_horizontal_distance(positions):
    start = positions[0]
    end = positions[-1]

    dx = end[0] - start[0]
    dy = end[1] - start[1]

    return np.sqrt(dx**2 + dy**2)