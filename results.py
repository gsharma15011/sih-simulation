import os
import csv
import numpy as np


def create_results_folder(folder="results"):
    os.makedirs(folder, exist_ok=True)
    return folder


def save_trajectory(times, positions, folder="results"):
    create_results_folder(folder)

    filepath = os.path.join(
        folder,
        "simulation_trajectory.csv"
    )

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Time",
            "X",
            "Y",
            "Z"
        ])

        for time, position in zip(times, positions):

            writer.writerow([
                time,
                position[0],
                position[1],
                position[2]
            ])

    return filepath


def save_monte_carlo_results(results, folder="results"):
    create_results_folder(folder)

    filepath = os.path.join(
        folder,
        "monte_carlo_results.csv"
    )

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Trial",
            "X",
            "Y",
            "Z"
        ])

        for index, position in enumerate(results, start=1):

            writer.writerow([
                index,
                position[0],
                position[1],
                position[2]
            ])

    return filepath


def save_summary(
    scenario_name,
    num_trials,
    max_height,
    total_time,
    horizontal_distance,
    mean,
    std,
    minimum,
    maximum,
    folder="results"
):

    create_results_folder(folder)

    filepath = os.path.join(
        folder,
        "summary.csv"
    )

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Metric",
            "Value"
        ])

        writer.writerow([
            "Scenario",
            scenario_name
        ])

        writer.writerow([
            "Monte Carlo Trials",
            num_trials
        ])

        writer.writerow([
            "Maximum Height",
            max_height
        ])

        writer.writerow([
            "Simulation Time",
            total_time
        ])

        writer.writerow([
            "Horizontal Distance",
            horizontal_distance
        ])

        writer.writerow([
            "Mean X",
            mean[0]
        ])

        writer.writerow([
            "Mean Y",
            mean[1]
        ])

        writer.writerow([
            "Mean Z",
            mean[2]
        ])

        writer.writerow([
            "Std X",
            std[0]
        ])

        writer.writerow([
            "Std Y",
            std[1]
        ])

        writer.writerow([
            "Std Z",
            std[2]
        ])

        writer.writerow([
            "Minimum X",
            minimum[0]
        ])

        writer.writerow([
            "Minimum Y",
            minimum[1]
        ])

        writer.writerow([
            "Minimum Z",
            minimum[2]
        ])

        writer.writerow([
            "Maximum X",
            maximum[0]
        ])

        writer.writerow([
            "Maximum Y",
            maximum[1]
        ])

        writer.writerow([
            "Maximum Z",
            maximum[2]
        ])

    return filepath


def save_text_report(
    scenario_name,
    num_trials,
    max_height,
    total_time,
    horizontal_distance,
    mean,
    std,
    folder="results"
):

    create_results_folder(folder)

    filepath = os.path.join(
        folder,
        "summary.txt"
    )

    with open(filepath, "w") as file:

        file.write(
            "TRAJECTORY SIMULATION REPORT\n"
        )

        file.write(
            "============================\n\n"
        )

        file.write(
            f"Scenario: {scenario_name}\n"
        )

        file.write(
            f"Monte Carlo Trials: {num_trials}\n\n"
        )

        file.write(
            "SINGLE SIMULATION\n"
        )

        file.write(
            "-----------------\n"
        )

        file.write(
            f"Maximum Height: {max_height:.4f}\n"
        )

        file.write(
            f"Simulation Time: {total_time:.4f}\n"
        )

        file.write(
            f"Horizontal Distance: "
            f"{horizontal_distance:.4f}\n\n"
        )

        file.write(
            "MONTE CARLO ANALYSIS\n"
        )

        file.write(
            "--------------------\n"
        )

        file.write(
            f"Mean Position: {mean}\n"
        )

        file.write(
            f"Standard Deviation: {std}\n"
        )

    return filepath