import numpy as np

from config import WIND_VELOCITY

GRAVITY = 9.81


def get_gravity():
    return np.array([0.0, 0.0, -GRAVITY])


def get_wind_velocity():
    return np.array(WIND_VELOCITY, dtype=float)