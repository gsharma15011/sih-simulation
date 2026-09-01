import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulation import run_simulation
from monte_carlo import run_monte_carlo
from scenarios import get_scenario


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SIH Simulation System",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 SIH Simulation & Uncertainty Analysis System")

st.write(
    "A software-based simulation environment for studying "
    "projectile trajectory behaviour under varying simulated "
    "environmental and sensor conditions."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Simulation Controls")

scenario_name = st.sidebar.selectbox(
    "Select Scenario",
    [
        "baseline",
        "wind",
        "sensor_noise"
    ]
)

num_trials = st.sidebar.slider(
    "Monte Carlo Trials",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

run_button = st.sidebar.button(
    "▶ Run Simulation",
    use_container_width=True
)


# =========================================================
# SCENARIO
# =========================================================

try:
    scenario = get_scenario(scenario_name)

except Exception as error:

    st.error(
        f"Could not load scenario: {error}"
    )

    st.stop()


# =========================================================
# SCENARIO INFORMATION
# =========================================================

st.subheader("Selected Scenario")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Scenario",
        scenario["name"]
    )

with col2:

    st.metric(
        "Initial Velocity",
        str(scenario["initial_velocity"])
    )

with col3:

    st.metric(
        "Wind",
        str(scenario["wind_velocity"])
    )


# =========================================================
# RUN SIMULATION
# =========================================================

if run_button:

    with st.spinner(
        "Running simulation and uncertainty analysis..."
    ):

        try:

            (
                times,
                positions,
                true_velocities,
                measured_velocities
            ) = run_simulation(
                initial_velocity=scenario["initial_velocity"],
                wind_velocity=scenario["wind_velocity"]
            )


            # -------------------------------------------------
            # MONTE CARLO
            # -------------------------------------------------

            monte_carlo_results = run_monte_carlo(
                num_trials=num_trials,
                initial_velocity=scenario["initial_velocity"],
                base_wind_velocity=scenario["wind_velocity"]
            )


            # -------------------------------------------------
            # STORE RESULTS
            # -------------------------------------------------

            st.session_state["times"] = times

            st.session_state["positions"] = positions

            st.session_state["monte_carlo"] = (
                monte_carlo_results
            )

            st.session_state["scenario"] = scenario_name

            st.success(
                "Simulation completed successfully."
            )

        except Exception as error:

            st.error(
                f"Simulation failed: {error}"
            )


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "positions" in st.session_state:

    positions = st.session_state["positions"]

    times = st.session_state["times"]

    monte_carlo_results = (
        st.session_state["monte_carlo"]
    )


    st.divider()

    st.header("Simulation Results")


    # =====================================================
    # BASIC METRICS
    # =====================================================

    max_height = np.max(
        positions[:, 2]
    )

    total_time = times[-1]

    horizontal_distance = np.sqrt(
        positions[-1, 0] ** 2 +
        positions[-1, 1] ** 2
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Maximum Height",
            f"{max_height:.2f}"
        )


    with col2:

        st.metric(
            "Simulation Time",
            f"{total_time:.2f}"
        )


    with col3:

        st.metric(
            "Horizontal Distance",
            f"{horizontal_distance:.2f}"
        )


    # =====================================================
    # 3D TRAJECTORY
    # =====================================================

    st.subheader("3D Trajectory")

    fig = plt.figure(
        figsize=(9, 6)
    )

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    ax.plot(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        linewidth=2
    )

    ax.scatter(
        positions[0, 0],
        positions[0, 1],
        positions[0, 2],
        marker="o",
        s=60,
        label="Start"
    )

    ax.scatter(
        positions[-1, 0],
        positions[-1, 1],
        positions[-1, 2],
        marker="x",
        s=80,
        label="End"
    )

    ax.set_xlabel("X Position")

    ax.set_ylabel("Y Position")

    ax.set_zlabel("Z Position")

    ax.set_title(
        "Simulated 3D Trajectory"
    )

    ax.legend()

    st.pyplot(fig)


    # =====================================================
    # MONTE CARLO DISPERSION
    # =====================================================

    st.subheader(
        "Monte Carlo Uncertainty Distribution"
    )

    mean_position = np.mean(
        monte_carlo_results,
        axis=0
    )


    fig2 = plt.figure(
        figsize=(9, 6)
    )

    ax2 = fig2.add_subplot(
        111,
        projection="3d"
    )

    ax2.scatter(
        monte_carlo_results[:, 0],
        monte_carlo_results[:, 1],
        monte_carlo_results[:, 2],
        alpha=0.6
    )

    ax2.scatter(
        mean_position[0],
        mean_position[1],
        mean_position[2],
        marker="x",
        s=150,
        label="Mean Position"
    )

    ax2.set_xlabel("X Position")

    ax2.set_ylabel("Y Position")

    ax2.set_zlabel("Z Position")

    ax2.set_title(
        "Monte Carlo Dispersion"
    )

    ax2.legend()

    st.pyplot(fig2)


    # =====================================================
    # STATISTICS
    # =====================================================

    st.subheader(
        "Uncertainty Statistics"
    )

    standard_deviation = np.std(
        monte_carlo_results,
        axis=0
    )

    minimum = np.min(
        monte_carlo_results,
        axis=0
    )

    maximum = np.max(
        monte_carlo_results,
        axis=0
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.write("**Mean Position**")

        st.write(
            np.round(
                mean_position,
                4
            )
        )


    with col2:

        st.write("**Standard Deviation**")

        st.write(
            np.round(
                standard_deviation,
                4
            )
        )


    with col3:

        st.write("**Observed Range**")

        st.write(
            np.round(
                maximum - minimum,
                4
            )
        )


    # =====================================================
    # RAW DATA
    # =====================================================

    st.subheader(
        "Monte Carlo Trial Data"
    )

    data = {

        "X": monte_carlo_results[:, 0],

        "Y": monte_carlo_results[:, 1],

        "Z": monte_carlo_results[:, 2]

    }

    st.dataframe(
        data,
        use_container_width=True
    )


    # =====================================================
    # CSV EXPORT
    # =====================================================

    csv_data = (
        "X,Y,Z\n"
    )

    for row in monte_carlo_results:

        csv_data += (
            f"{row[0]},"
            f"{row[1]},"
            f"{row[2]}\n"
        )


    st.download_button(

        label="⬇ Download Monte Carlo Results",

        data=csv_data,

        file_name="monte_carlo_results.csv",

        mime="text/csv"

    )

else:

    st.info(
        "Select a scenario and click "
        "'Run Simulation' to begin."
    )