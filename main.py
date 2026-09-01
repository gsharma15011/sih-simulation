from simulation import run_simulation
from monte_carlo import run_monte_carlo

from scenarios import get_scenario

from metrics import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_minimum,
    calculate_maximum,
    calculate_max_height,
    calculate_total_time,
    calculate_horizontal_distance
)

from plots import plot_simulation_results


# =================================================
# SELECT SCENARIO
# =================================================

SCENARIO_NAME = "baseline"

scenario = get_scenario(SCENARIO_NAME)


print()
print("==========================================")
print("          SELECTED SCENARIO")
print("==========================================")

print("Scenario:", scenario["name"])
print("Initial velocity:", scenario["initial_velocity"])
print("Wind velocity:", scenario["wind_velocity"])


# =================================================
# SINGLE SIMULATION
# =================================================

(
    times,
    positions,
    true_velocities,
    measured_velocities
) = run_simulation(
    initial_velocity=scenario["initial_velocity"],
    wind_velocity=scenario["wind_velocity"]
)


# =================================================
# SINGLE SIMULATION METRICS
# =================================================

max_height = calculate_max_height(positions)

total_time = calculate_total_time(times)

horizontal_distance = calculate_horizontal_distance(
    positions
)


# =================================================
# MONTE CARLO
# =================================================

NUM_TRIALS = 100

results = run_monte_carlo(
    num_trials=NUM_TRIALS,
    initial_velocity=scenario["initial_velocity"],
    base_wind_velocity=scenario["wind_velocity"]
)


# =================================================
# MONTE CARLO METRICS
# =================================================

mean = calculate_mean(results)

std = calculate_standard_deviation(results)

minimum = calculate_minimum(results)

maximum = calculate_maximum(results)


# =================================================
# PRINT SINGLE SIMULATION RESULTS
# =================================================

print()
print("==========================================")
print("       TRAJECTORY SIMULATION RESULTS")
print("==========================================")

print(f"Maximum height:       {max_height:.3f}")

print(f"Simulation time:      {total_time:.3f}")

print(
    f"Horizontal distance:  "
    f"{horizontal_distance:.3f}"
)


# =================================================
# PRINT MONTE CARLO RESULTS
# =================================================

print()
print("==========================================")
print("       MONTE CARLO ANALYSIS")
print("==========================================")

print(f"Number of trials:     {NUM_TRIALS}")

print(f"Mean position:        {mean}")

print(f"Standard deviation:   {std}")

print(f"Minimum position:     {minimum}")

print(f"Maximum position:     {maximum}")


# =================================================
# VISUALIZATION
# =================================================

plot_simulation_results(
    positions,
    results,
    mean
)
