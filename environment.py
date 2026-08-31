import numpy as np

GRAVITY = 9.81


def get_gravity():
    return np.array([0.0, 0.0, -GRAVITY])