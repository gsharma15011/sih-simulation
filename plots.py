import matplotlib.pyplot as plt


def plot_trajectory(positions):

    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(x, y, z)

    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_zlabel("Z Position")
    ax.set_title("3D Trajectory Simulation")

    plt.show()


def plot_monte_carlo_results(results, mean):

    x = results[:, 0]
    y = results[:, 1]
    z = results[:, 2]

    fig = plt.figure(figsize=(10, 7))

    ax = fig.add_subplot(111, projection="3d")

    # Plot every Monte Carlo result
    ax.scatter(x, y, z)

    # Plot the mean position
    ax.scatter(
        mean[0],
        mean[1],
        mean[2],
        marker="X",
        s=150,
        label="Mean Position"
    )

    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_zlabel("Z Position")

    ax.set_title("3D Monte Carlo Dispersion")

    ax.legend()

    plt.show()