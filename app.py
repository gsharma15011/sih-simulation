import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from unity_export import export_trajectory

from scenarios import get_scenario
from simulation import run_simulation
from monte_carlo import run_monte_carlo
from visualization import create_3d_visualization

from metrics import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_minimum,
    calculate_maximum,
    calculate_max_height,
    calculate_total_time,
    calculate_horizontal_distance
)

from results import (
    save_trajectory,
    save_monte_carlo_results,
    save_summary,
    save_text_report
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Trajectory Simulation System",
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
            "Simulation with relatively low environmental disturbance."
    },

    "high_wind": {
        "title": "High Wind",
        "description":
            "Simulation with stronger simulated wind disturbance."
    },

    "cross_wind": {
        "title": "Cross Wind",
        "description":
            "Simulation with environmental disturbance acting across the trajectory."
    }
}


# =========================================================
# TITLE
# =========================================================

st.title("🚀 Trajectory Simulation & Uncertainty Analysis")

st.write(
    "A software-based prototype for numerical trajectory simulation, "
    "environmental scenario analysis and Monte Carlo uncertainty analysis."
)

st.divider()


# =========================================================
# SIDEBAR
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
    "▶ Run Complete Analysis",
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
# RUN COMPLETE ANALYSIS
# =========================================================

if run_button:

    with st.spinner(
        "Running simulation, Monte Carlo analysis and result export..."
    ):

        try:

            # ---------------------------------------------
            # SINGLE SIMULATION
            # ---------------------------------------------

            (
                times,
                positions,
                true_velocities,
                measured_velocities
            ) = run_simulation(
                initial_velocity=scenario["initial_velocity"],
                wind_velocity=scenario["wind_velocity"]
            )
            export_trajectory(
                  times,
                 positions
            )


            # ---------------------------------------------
            # SINGLE SIMULATION METRICS
            # ---------------------------------------------

            max_height = calculate_max_height(
                positions
            )

            total_time = calculate_total_time(
                times
            )

            horizontal_distance = (
                calculate_horizontal_distance(
                    positions
                )
            )


            # ---------------------------------------------
            # MONTE CARLO SIMULATION
            # ---------------------------------------------

            monte_carlo_results = run_monte_carlo(
                num_trials=num_trials,
                initial_velocity=scenario["initial_velocity"],
                base_wind_velocity=scenario["wind_velocity"]
            )


            # ---------------------------------------------
            # MONTE CARLO METRICS
            # ---------------------------------------------

            mean_position = calculate_mean(
                monte_carlo_results
            )

            standard_deviation = (
                calculate_standard_deviation(
                    monte_carlo_results
                )
            )

            minimum = calculate_minimum(
                monte_carlo_results
            )

            maximum = calculate_maximum(
                monte_carlo_results
            )


            # ---------------------------------------------
            # SAVE RESULTS
            # ---------------------------------------------

            save_trajectory(
                times,
                positions
            )

            save_monte_carlo_results(
                monte_carlo_results
            )

            save_summary(
                scenario_name=scenario["name"],
                num_trials=num_trials,
                max_height=max_height,
                total_time=total_time,
                horizontal_distance=horizontal_distance,
                mean=mean_position,
                std=standard_deviation,
                minimum=minimum,
                maximum=maximum
            )

            save_text_report(
                scenario_name=scenario["name"],
                num_trials=num_trials,
                max_height=max_height,
                total_time=total_time,
                horizontal_distance=horizontal_distance,
                mean=mean_position,
                std=standard_deviation
            )


            # ---------------------------------------------
            # STORE EVERYTHING
            # ---------------------------------------------

            st.session_state["results"] = {

                "times": times,

                "positions": positions,

                "monte_carlo": monte_carlo_results,

                "max_height": max_height,

                "total_time": total_time,

                "horizontal_distance": horizontal_distance,

                "mean": mean_position,

                "std": standard_deviation,

                "minimum": minimum,

                "maximum": maximum,

                "num_trials": num_trials,

                "scenario_name": scenario["name"]

            }


            st.success(
                "Complete analysis finished successfully!"
            )

        except Exception as error:

            st.error(
                f"Simulation failed: {error}"
            )


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    positions = results["positions"]
    times = results["times"]
    monte_carlo_results = results["monte_carlo"]

    st.divider()

    st.header("📊 Analysis Results")


    # =====================================================
    # METRIC CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Maximum Height",
            f"{results['max_height']:.2f}"
        )

    with col2:
        st.metric(
            "Simulation Time",
            f"{results['total_time']:.2f}"
        )

    with col3:
        st.metric(
            "Horizontal Distance",
            f"{results['horizontal_distance']:.2f}"
        )

    with col4:
        st.metric(
            "Monte Carlo Trials",
            results["num_trials"]
        )


    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📈 Trajectory",
            "🎯 Uncertainty",
            "📊 Statistics",
            "📁 Raw Data"
        ]
    )


    # =====================================================
    # TRAJECTORY TAB
    # =====================================================

    with tab1:


       st.subheader("3D Simulated Trajectory")

       st.write(
            "The trajectory is calculated by numerically updating "
            "position and velocity over small time intervals."
        )

        # Interactive 3D Digital Twin
       fig = create_3d_visualization(
            positions,
            title="3D Trajectory Digital Twin"
        )

       st.plotly_chart(
            fig,
            use_container_width=True,
            key="trajectory_plot"
        )


    # =====================================================
    # UNCERTAINTY TAB
    # =====================================================

    with tab2:

        st.subheader(
            "Monte Carlo Uncertainty Analysis"
        )

        st.write(
            "The simulation is repeated multiple times with random "
            "variation in simulated environmental conditions."
        )

        fig2 = plt.figure(figsize=(10, 7))

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
            results["mean"][0],
            results["mean"][1],
            results["mean"][2],
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
            "Each point represents one simulation outcome. "
            "The X marker represents the mean outcome."
        )


    # =====================================================
    # STATISTICS TAB
    # =====================================================

    with tab3:

        st.subheader("Statistical Analysis")

        observed_range = (
            results["maximum"]
            -
            results["minimum"]
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
                        results["mean"],
                        4
                    )

                }),

                hide_index=True,
                use_container_width=True
            )


        with stat_col2:

            st.write(
                "### Standard Deviation"
            )

            st.dataframe(
                pd.DataFrame({

                    "Axis": ["X", "Y", "Z"],

                    "Value": np.round(
                        results["std"],
                        4
                    )

                }),

                hide_index=True,
                use_container_width=True
            )


        with stat_col3:

            st.write("### Observed Range")

            st.dataframe(
                pd.DataFrame({

                    "Axis": ["X", "Y", "Z"],

                    "Value": np.round(
                        observed_range,
                        4
                    )

                }),

                hide_index=True,
                use_container_width=True
            )


        st.info(
            "Higher standard deviation means the repeated simulation "
            "outcomes are more widely spread."
        )


    # =====================================================
    # RAW DATA TAB
    # =====================================================

    with tab4:

        st.subheader(
            "Monte Carlo Trial Results"
        )

        dataframe = pd.DataFrame({

            "Trial": range(
                1,
                len(monte_carlo_results) + 1
            ),

            "X": monte_carlo_results[:, 0],

            "Y": monte_carlo_results[:, 1],

            "Z": monte_carlo_results[:, 2]

        })

        st.dataframe(
            dataframe,
            use_container_width=True,
            height=400
        )

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
        "👈 Select a scenario, choose the number of trials "
        "and click **Run Complete Analysis**."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SIH Prototype • Numerical Simulation • "
    "Scenario Analysis • Monte Carlo Uncertainty Analysis"
)