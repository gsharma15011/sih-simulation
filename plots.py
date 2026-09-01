import matplotlib.pyplot as plt


def plot_simulation_results(positions, results, mean):

    fig = plt.figure(figsize=(14, 7))

    # -------------------------------------------------
    # LEFT: SINGLE 3D TRAJECTORY
    # -------------------------------------------------

    ax1 = fig.add_subplot(121, projection="3d")

    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]

    ax1.plot(x, y, z, linewidth=2)

    # Starting point
    ax1.scatter(
        x[0],
        y[0],
        z[0],
        s=80,
        label="Start"
    )

    # Ending point
    ax1.scatter(
        x[-1],
        y[-1],
        z[-1],
        s=80,
        label="End"
    )

    ax1.set_xlabel("X Position")
    ax1.set_ylabel("Y Position")
    ax1.set_zlabel("Z Position")

    ax1.set_title("3D Trajectory")

    ax1.legend()


    # -------------------------------------------------
    # RIGHT: MONTE CARLO DISPERSION
    # -------------------------------------------------

    ax2 = fig.add_subplot(122, projection="3d")

    rx = results[:, 0]
    ry = results[:, 1]
    rz = results[:, 2]

    ax2.scatter(
        rx,
        ry,
        rz,
        s=25,
        alpha=0.7,
        label="Simulation Trials"
    )

    # Mean position
    ax2.scatter(
        mean[0],
        mean[1],
        mean[2],
        marker="X",
        s=180,
        label="Mean Position"
    )

    ax2.set_xlabel("X Position")
    ax2.set_ylabel("Y Position")
    ax2.set_zlabel("Z Position")

    ax2.set_title("Monte Carlo Dispersion")

    ax2.legend()


    # -------------------------------------------------
    # OVERALL TITLE
    # -------------------------------------------------

    fig.suptitle(
        "Trajectory Simulation & Uncertainty Analysis",
        fontsize=16
    )

    plt.tight_layout()

    plt.show()