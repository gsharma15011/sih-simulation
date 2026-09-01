import streamlit as st
import numpy as np
import pandas as pd
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
# SCENARIO INFORMATION
# =========================================================

SCENARIO_INFO = {

    "baseline": {
        "title": "Baseline",
        "description":
            "Standard simulated environmental conditions."
    },

    "low_wind": {
        "title": "Low Wind",
        "description":
            "Simulation with relatively low wind disturbance."
    },

    "high_wind": {
        "title": "High Wind",
        "description":
            "Simulation with stronger environmental disturbance."
    },

    "cross_wind": {
        "title": "Cross Wind",
        "description":
            "Simulation with wind acting primarily across the trajectory."
    }

}


# =========================================================
# TITLE
# =========================================================

st.title("🚀 Trajectory Simulation & Uncertainty Analysis")

st.write(
    "A software-based simulation prototype for analysing "
    "trajectory behaviour under different simulated environmental "
    "conditions and studying uncertainty using Monte Carlo analysis."
)

st.divider()


# =========================================================
# SIDEBAR CONTROLS
# =========================================================

st.sidebar.header("⚙️ Simulation Controls")

scenario_name = st.sidebar.selectbox(
    "Select Scenario",
    list(SCENARIO_INFO.keys()),
    format_func=lambda x: SCENARIO_INFO[x]["title"]
)


num_trials = st.sidebar.slider(
    "Monte Carlo Trials",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)


run_button = st.sidebar.button(
    "▶ Run Analysis",
    use_container_width=True
)


# =========================================================
# LOAD SCENARIO
# =========================================================

scenario = get_scenario(scenario_name)


# =========================================================
# SCENARIO OVERVIEW
# =========================================================

st.subheader("📌 Selected Scenario")

st.info(
    SCENARIO_INFO[scenario_name]["description"]
)


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
        "Wind Velocity",
        str(scenario["wind_velocity"])
    )


# =========================================================
# RUN SIMULATION
# =========================================================

if run_button:

    with st.spinner(
        "Running trajectory simulation and Monte Carlo analysis..."
    ):

        try:

            # -------------------------------------------------
            # SINGLE SIMULATION
            # -------------------------------------------------

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

            st.session_state["scenario_name"] = (
                scenario_name
            )

            st.session_state["num_trials"] = (
                num_trials
            )

            st.success(
                "Analysis completed successfully!"
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


    # =====================================================
    # CALCULATE METRICS
    # =====================================================

    max_height = np.max(
        positions[:, 2]
    )

    total_time = times[-1]

    horizontal_distance = np.sqrt(
        positions[-1, 0] ** 2
        +
        positions[-1, 1] ** 2
    )

    mean_position = np.mean(
        monte_carlo_results,
        axis=0
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


    # =====================================================
    # RESULTS HEADER
    # =====================================================

    st.divider()

    st.header("📊 Simulation Results")


    # =====================================================
    # METRIC CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


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


    with col4:

        st.metric(
            "Monte Carlo Trials",
            st.session_state["num_trials"]
        )


    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs(

        [
            "📈 Trajectory",
            "🎯 Uncertainty Analysis",
            "📊 Statistics",
            "📁 Raw Data"
        ]

    )


    # =====================================================
    # TAB 1: TRAJECTORY
    # =====================================================

    with tab1:

        st.subheader("3D Simulated Trajectory")

        st.write(
            "This visualization shows the simulated position "
            "of the object over time along the X, Y and Z axes."
        )


        fig = plt.figure(
            figsize=(10, 7)
        )

        ax = fig.add_subplot(
            111,
            projection="3d"
        )


        ax.plot(

            positions[:, 0],

            positions[:, 1],

            positions[:, 2],

            linewidth=2,

            label="Trajectory"

        )


        # Start

        ax.scatter(

            positions[0, 0],

            positions[0, 1],

            positions[0, 2],

            s=80,

            marker="o",

            label="Start"

        )


        # End

        ax.scatter(

            positions[-1, 0],

            positions[-1, 1],

            positions[-1, 2],

            s=100,

            marker="X",

            label="End"

        )


        ax.set_xlabel("X Position")

        ax.set_ylabel("Y Position")

        ax.set_zlabel("Z Position")

        ax.set_title(
            "3D Trajectory Simulation"
        )

        ax.legend()

        st.pyplot(fig)


        st.caption(
            "The trajectory is generated numerically by updating "
            "position and velocity over small time intervals."
        )


    # =====================================================
    # TAB 2: MONTE CARLO
    # =====================================================

    with tab2:

        st.subheader(
            "Monte Carlo Uncertainty Distribution"
        )

        st.write(
            "The simulation is repeated multiple times with "
            "random variation in simulated environmental conditions."
        )


        fig2 = plt.figure(
            figsize=(10, 7)
        )

        ax2 = fig2.add_subplot(
            111,
            projection="3d"
        )


        ax2.scatter(

            monte_carlo_results[:, 0],

            monte_carlo_results[:, 1],

            monte_carlo_results[:, 2],

            alpha=0.6,

            label="Simulation Trials"

        )


        ax2.scatter(

            mean_position[0],

            mean_position[1],

            mean_position[2],

            marker="X",

            s=200,

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


        st.caption(
            "Each point represents the final result of one simulation trial. "
            "The X marker represents the average result."
        )


    # =====================================================
    # TAB 3: STATISTICS
    # =====================================================

    with tab3:

        st.subheader(
            "Statistical Analysis"
        )


        stat_col1, stat_col2, stat_col3 = (
            st.columns(3)
        )


        with stat_col1:

            st.write("### Mean Position")

            st.dataframe(

                pd.DataFrame({

                    "Axis": ["X", "Y", "Z"],

                    "Value": np.round(
                        mean_position,
                        4
                    )

                }),

                use_container_width=True,

                hide_index=True

            )


        with stat_col2:

            st.write(
                "### Standard Deviation"
            )

            st.dataframe(

                pd.DataFrame({

                    "Axis": ["X", "Y", "Z"],

                    "Value": np.round(
                        standard_deviation,
                        4
                    )

                }),

                use_container_width=True,

                hide_index=True

            )


        with stat_col3:

            st.write("### Observed Range")

            observed_range = (
                maximum - minimum
            )

            st.dataframe(

                pd.DataFrame({

                    "Axis": ["X", "Y", "Z"],

                    "Value": np.round(
                        observed_range,
                        4
                    )

                }),

                use_container_width=True,

                hide_index=True

            )


        st.info(

            "A higher standard deviation indicates greater variation "
            "between repeated simulation outcomes."

        )


    # =====================================================
    # TAB 4: RAW DATA
    # =====================================================

    with tab4:

        st.subheader(
            "Monte Carlo Trial Results"
        )


        dataframe = pd.DataFrame({

            "Trial":

                range(
                    1,
                    len(monte_carlo_results) + 1
                ),

            "X":

                monte_carlo_results[:, 0],

            "Y":

                monte_carlo_results[:, 1],

            "Z":

                monte_carlo_results[:, 2]

        })


        st.dataframe(

            dataframe,

            use_container_width=True,

            height=400

        )


        # =================================================
        # DOWNLOAD CSV
        # =================================================

        csv = dataframe.to_csv(
            index=False
        )


        st.download_button(

            label="⬇ Download Monte Carlo Results",

            data=csv,

            file_name="monte_carlo_results.csv",

            mime="text/csv",

            use_container_width=True

        )


else:

    st.info(
        "👈 Select a scenario, choose the number of Monte Carlo "
        "trials and click **Run Analysis**."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SIH Prototype • Numerical Simulation • "
    "Monte Carlo Uncertainty Analysis"
)