from simulation import run_simulation
from plots import plot_trajectory


times, positions, true_velocities, measured_velocities = run_simulation()

plot_trajectory(positions)