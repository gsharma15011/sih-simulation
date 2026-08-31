import numpy as np

from config import DT, TOTAL_TIME, INITIAL_POSITION, INITIAL_VELOCITY
from physics import calculate_acceleration
from sensors import measure_velocity


def run_simulation():
    true_velocities =[]
    measured_velocities = []
    position = np.array(INITIAL_POSITION, dtype=float)
    velocity = np.array(INITIAL_VELOCITY, dtype=float)

    positions = []
    times = []

    time = 0.0

    while time <= TOTAL_TIME:

        positions.append(position.copy())
        times.append(time)

        acceleration = calculate_acceleration(velocity)

        measured_velocity = measure_velocity(velocity)
        true_velocities.append(velocity.copy())
        velocity = velocity + acceleration * DT
        measured_velocities.append(measured_velocity)

        position = position + velocity * DT

        if position[2]<0:
            break

        time = time + DT

    return (
        np.array(times), 
        np.array(positions),
        np.array(true_velocities), 
        np.array(measured_velocities)

    )