import json
import os


def export_trajectory(
    times,
    positions,
    filename="trajectory.json"
):
    """
    Export trajectory simulation data
    into a JSON file for Unity.
    """

    data = {
        "points": []
    }

    for i in range(len(positions)):

        point = {
            "time": float(times[i]),
            "x": float(positions[i][0]),
            "y": float(positions[i][1]),
            "z": float(positions[i][2])
        }

        data["points"].append(point)

    output_path = os.path.join(
        os.path.dirname(__file__),
        filename
    )

    with open(output_path, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(
        f"Trajectory exported successfully: {output_path}"
    )

    return output_path