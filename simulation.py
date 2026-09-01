import numpy as np

from config import (
    INITIAL_POSITION,
    INITIAL_VELOCITY,
    TIME_STEP,
    MAX_TIME
)

from physics import calculate_acceleration
from sensors import measure_velocity


def run_simulation(
    initial_velocity=None,
    wind_velocity=None
):

    # ---------------------------------------------
    # INITIAL CONDITIONS
    # ---------------------------------------------

    position = np.array(
        INITIAL_POSITION,
        dtype=float
    )

    if initial_velocity is None:
        initial_velocity = INITIAL_VELOCITY

    velocity = np.array(
        initial_velocity,
        dtype=float
    )

    time = 0.0


    # ---------------------------------------------
    # STORAGE
    # ---------------------------------------------

    times = []
    positions = []

    true_velocities = []
    measured_velocities = []


    # ---------------------------------------------
    # SIMULATION LOOP
    # ---------------------------------------------

    while time <= MAX_TIME and position[2] >= 0:

        times.append(time)

        positions.append(position.copy())

        true_velocities.append(
            velocity.copy()
        )

        measured_velocity = measure_velocity(
            velocity
        )

        measured_velocities.append(
            measured_velocity
        )


        # Calculate acceleration

        acceleration = calculate_acceleration(
            velocity,
            wind_velocity
        )


        # Update velocity

        velocity = velocity + acceleration * TIME_STEP


        # Update position

        position = position + velocity * TIME_STEP


        # Update time

        time += TIME_STEP


    # ---------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------

    return (
        np.array(times),
        np.array(positions),
        np.array(true_velocities),
        np.array(measured_velocities)
    )
