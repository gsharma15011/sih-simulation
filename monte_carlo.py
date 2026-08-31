import numpy as np 
from simulation import run_simulation

def run_monte_carlo(num_trials=100):
    results = []
    for trial in range(num_trials):

        #Generate a slightly different wind condition
        wind_x = np.random.normal(2.0, 0.5)
        wind_y = np.random.normal(1.5, 0.5)

        wind_velocity= [wind_x, wind_y, 0.0]

        #Run the simulation with this trial's environment

        times, positions, true_velocities, measured_velocities = run_simulation(wind_velocity=wind_velocity)

        #Stroe the final position 
        final_position = positions[-1]
        results.append(final_position)
    return np.array(results)

