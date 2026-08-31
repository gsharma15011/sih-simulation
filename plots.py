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