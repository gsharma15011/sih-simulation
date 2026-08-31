import numpy as np

from config import WIND_VELOCITY

GRAVITY = 9.81


def get_gravity():
    return np.array([0.0, 0.0, -GRAVITY])


def get_wind_velocity(wind_velocity=None):
    if wind_velocity is None:
        wind_velocity = WIND_VELOCITY

    return np.array(wind_velocity, dtype=float)