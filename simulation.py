import numpy as np

from config import DT, TOTAL_TIME, INITIAL_POSITION, INITIAL_VELOCITY
from physics import calculate_acceleration


def run_simulation():

    position = np.array(INITIAL_POSITION, dtype=float)
    velocity = np.array(INITIAL_VELOCITY, dtype=float)

    positions = []
    times = []

    time = 0.0

    while time <= TOTAL_TIME:

        positions.append(position.copy())
        times.append(time)

        acceleration = calculate_acceleration()

        velocity = velocity + acceleration * DT

        position = position + velocity * DT

        if position[2]<0:
            break

        time = time + DT

    return np.array(times), np.array(positions)