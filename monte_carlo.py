import numpy as np

from simulation import run_simulation


def run_monte_carlo(
    num_trials=100,
    initial_velocity=None,
    base_wind_velocity=None
):

    results = []

    if base_wind_velocity is None:
        base_wind_velocity = [2.0, 1.5, 0.0]


    for trial in range(num_trials):

        # -----------------------------------------
        # RANDOM ENVIRONMENT FOR THIS TRIAL
        # -----------------------------------------

        wind_x = np.random.normal(
            base_wind_velocity[0],
            0.5
        )

        wind_y = np.random.normal(
            base_wind_velocity[1],
            0.5
        )

        wind_velocity = [
            wind_x,
            wind_y,
            base_wind_velocity[2]
        ]


        # -----------------------------------------
        # RUN SIMULATION
        # -----------------------------------------

        (
            times,
            positions,
            true_velocities,
            measured_velocities
        ) = run_simulation(
            initial_velocity=initial_velocity,
            wind_velocity=wind_velocity
        )


        # -----------------------------------------
        # STORE FINAL POSITION
        # -----------------------------------------

        final_position = positions[-1]

        results.append(final_position)


    return np.array(results)