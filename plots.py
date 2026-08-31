import matplotlib.pyplot as plt


def plot_trajectory(positions):

    x = positions[:, 0]
    z = positions[:, 2]

    plt.plot(x, z)

    plt.xlabel("X Position")
    plt.ylabel("Z Position")

    plt.title("Simulated Trajectory")

    plt.grid()

    plt.show()