from monte_carlo import run_monte_carlo

from metrics import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_minimum,
    calculate_maximum
)

from plots import plot_monte_carlo_results


results = run_monte_carlo(100)

mean = calculate_mean(results)
std = calculate_standard_deviation(results)
minimum = calculate_minimum(results)
maximum = calculate_maximum(results)


print("Number of trials:", len(results))
print("Mean position:", mean)
print("Standard deviation:", std)
print("Minimum position:", minimum)
print("Maximum position:", maximum)


plot_monte_carlo_results(results, mean)