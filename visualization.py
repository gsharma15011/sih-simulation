import numpy as np
import plotly.graph_objects as go


def create_3d_visualization(
    positions,
    monte_carlo_results=None,
    title="3D Trajectory Digital Twin"
):
    """
    Create an interactive 3D visualization.

    positions:
        Array containing trajectory coordinates:
        [x, y, z]

    monte_carlo_results:
        Optional array containing final positions from
        repeated simulation trials.
    """

    positions = np.asarray(positions)

    fig = go.Figure()

    # --------------------------------------------------
    # 1. GROUND / TERRAIN
    # --------------------------------------------------

    if len(positions) > 0:

        x_min = float(np.min(positions[:, 0]))
        x_max = float(np.max(positions[:, 0]))

        y_min = float(np.min(positions[:, 1]))
        y_max = float(np.max(positions[:, 1]))

        # Add some margin around trajectory
        x_margin = max((x_max - x_min) * 0.15, 5)
        y_margin = max((y_max - y_min) * 0.15, 5)

        terrain_x = np.linspace(
            x_min - x_margin,
            x_max + x_margin,
            25
        )

        terrain_y = np.linspace(
            y_min - y_margin,
            y_max + y_margin,
            25
        )

        X, Y = np.meshgrid(
            terrain_x,
            terrain_y
        )

        # Slightly uneven ground surface
        Z = (
            0.15 * np.sin(X / 8)
            + 0.15 * np.cos(Y / 8)
        )

        fig.add_trace(
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                opacity=0.45,
                showscale=False,
                name="Terrain"
            )
        )

    # --------------------------------------------------
    # 2. MAIN TRAJECTORY
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],

            mode="lines",

            line=dict(
                width=7
            ),

            name="Simulated Trajectory"
        )
    )

    # --------------------------------------------------
    # 3. START POINT
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=[positions[0, 0]],
            y=[positions[0, 1]],
            z=[positions[0, 2]],

            mode="markers+text",

            marker=dict(
                size=8
            ),

            text=["START"],
            textposition="top center",

            name="Start"
        )
    )

    # --------------------------------------------------
    # 4. END POINT
    # --------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=[positions[-1, 0]],
            y=[positions[-1, 1]],
            z=[positions[-1, 2]],

            mode="markers+text",

            marker=dict(
                size=10
            ),

            text=["END"],
            textposition="top center",

            name="End"
        )
    )

    # --------------------------------------------------
    # 5. MONTE CARLO DISPERSION
    # --------------------------------------------------

    if monte_carlo_results is not None:

        monte_carlo_results = np.asarray(
            monte_carlo_results
        )

        if len(monte_carlo_results) > 0:

            fig.add_trace(
                go.Scatter3d(

                    x=monte_carlo_results[:, 0],
                    y=monte_carlo_results[:, 1],
                    z=monte_carlo_results[:, 2],

                    mode="markers",

                    marker=dict(
                        size=4,
                        opacity=0.55
                    ),

                    name="Simulation Trials"
                )
            )

            # Mean position
            mean_position = np.mean(
                monte_carlo_results,
                axis=0
            )

            fig.add_trace(
                go.Scatter3d(

                    x=[mean_position[0]],
                    y=[mean_position[1]],
                    z=[mean_position[2]],

                    mode="markers+text",

                    marker=dict(
                        size=12,
                        symbol="diamond"
                    ),

                    text=["MEAN"],
                    textposition="top center",

                    name="Mean Position"
                )
            )

    # --------------------------------------------------
    # 6. LAYOUT
    # --------------------------------------------------

    fig.update_layout(

        title={
            "text": title,
            "x": 0.5
        },

        scene=dict(

            xaxis_title="X Position",

            yaxis_title="Y Position",

            zaxis_title="Z Position",

            aspectmode="auto",

            camera=dict(
                eye=dict(
                    x=1.6,
                    y=1.6,
                    z=1.2
                )
            )
        ),

        height=700,

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        ),

        legend=dict(
            x=0.02,
            y=0.98
        )
    )

    return fig