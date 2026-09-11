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

    while time <= MAX_TIME:

        # Store current state

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


        # -----------------------------------------
        # CALCULATE ACCELERATION
        # -----------------------------------------

        acceleration = calculate_acceleration(
            velocity,
            wind_velocity
        )


        # -----------------------------------------
        # CALCULATE NEXT STATE
        # -----------------------------------------

        next_velocity = (
            velocity +
            acceleration * TIME_STEP
        )

        next_position = (
            position +
            next_velocity * TIME_STEP
        )

        next_time = time + TIME_STEP


        # -----------------------------------------
        # GROUND INTERSECTION
        # -----------------------------------------

        if (
            position[2] > 0
            and next_position[2] <= 0
        ):

            # Fraction of the time step at which
            # the trajectory reaches ground

            alpha = (
                position[2] /
                (position[2] - next_position[2])
            )

            # Exact impact position

            impact_position = (
                position +
                alpha *
                (next_position - position)
            )

            # Force exact ground level

            impact_position[2] = 0.0

            # Exact impact time

            impact_time = (
                time +
                alpha * TIME_STEP
            )

            # Store impact point

            times.append(impact_time)

            positions.append(
                impact_position.copy()
            )

            true_velocities.append(
                next_velocity.copy()
            )

            measured_velocities.append(
                measure_velocity(next_velocity)
            )

            break


        # -----------------------------------------
        # UPDATE STATE
        # -----------------------------------------

        velocity = next_velocity

        position = next_position

        time = next_time


    # ---------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------

    return (
        np.array(times),
        np.array(positions),
        np.array(true_velocities),
        np.array(measured_velocities)
    )