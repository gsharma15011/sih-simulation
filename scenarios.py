SCENARIOS = {

    "baseline": {
        "name": "Baseline",
        "initial_velocity": [10.0, 4.0, 20.0],
        "wind_velocity": [2.0, 1.5, 0.0]
    },

    "low_wind": {
        "name": "Low Wind",
        "initial_velocity": [10.0, 4.0, 20.0],
        "wind_velocity": [0.5, 0.3, 0.0]
    },

    "high_wind": {
        "name": "High Wind",
        "initial_velocity": [10.0, 4.0, 20.0],
        "wind_velocity": [5.0, 3.0, 0.0]
    },

    "cross_wind": {
        "name": "Cross Wind",
        "initial_velocity": [10.0, 4.0, 20.0],
        "wind_velocity": [0.0, 4.0, 0.0]
    }

}


def get_scenario(scenario_name):

    if scenario_name not in SCENARIOS:
        raise ValueError(
            f"Scenario '{scenario_name}' not found."
        )

    return SCENARIOS[scenario_name]