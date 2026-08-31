from simulation import run_simulation
from plots import plot_trajectory


times, positions = run_simulation()

plot_trajectory(positions)