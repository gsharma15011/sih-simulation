import numpy as np

from config import VELOCITY_NOISE_STD

def measure_velocity(true_velocity):
    noise = np.random.normal(
        0,
        VELOCITY_NOISE_STD,
        size=3
    )
    measured_velocity = true_velocity + noise
    return measured_velocity