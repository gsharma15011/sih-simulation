from monte_carlo import run_monte_carlo

from metrics import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_minimum,
    calculate_maximum,
    calculate_max_height,
    calculate_total_time,
    calculate_horizontal_distance
)

from simulation import run_simulation


# -------------------------------------------------
# SINGLE SIMULATION
# -------------------------------------------------

times, positions, true_velocities, measured_velocities = run_simulation()

print("\n========== SINGLE SIMULATION ==========")

max_height = calculate_max_height(positions)
total_time = calculate_total_time(times)
horizontal_distance = calculate_horizontal_distance(positions)

print("Maximum height:", max_height)
print("Total simulation time:", total_time)
print("Horizontal distance:", horizontal_distance)


# -------------------------------------------------
# MONTE CARLO SIMULATION
# -------------------------------------------------

results = run_monte_carlo(100)

mean = calculate_mean(results)
std = calculate_standard_deviation(results)
minimum = calculate_minimum(results)
maximum = calculate_maximum(results)

print("\n========== MONTE CARLO ANALYSIS ==========")

print("Number of trials:", len(results))

print("Mean final position:", mean)

print("Standard deviation:", std)

print("Minimum final position:", minimum)

print("Maximum final position:", maximum)