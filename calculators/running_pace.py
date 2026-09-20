import streamlit as st

from utils.calculations import (
    pace_to_speed,
    distance_and_time_to_pace,
    format_pace,
)


# Standard running distances.
# Values are stored as (distance, unit).
STANDARD_DISTANCES = {
    "5K": (5.0, "km"),
    "10K": (10.0, "km"),
    "Half Marathon": (21.0975, "km"),
    "Marathon": (42.195, "km"),
    "50K": (50.0, "km"),
    "100K": (100.0, "km"),
}


def render_running_pace_calculator():

    st.markdown(
        '<div class="main-title">'
        "🏃 Running Pace & Speed Calculator"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Convert running pace to speed, or calculate the pace "
        "and speed required to achieve a target finishing time."
        "</div>",
        unsafe_allow_html=True,
    )

    # =====================================================
    # SECTION 1 — PACE TO SPEED
    # =====================================================

    st.subheader("🏃 Pace → Speed")

    st.write(
        "Enter your running pace and see the equivalent speed "
        "in both kilometres per hour and miles per hour."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        pace_minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=6,
            step=1,
            key="running_pace_minutes",
        )

    with col2:
        pace_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            key="running_pace_seconds",
        )

    with col3:
        pace_unit = st.selectbox(
            "Pace unit",
            ["km", "mile"],
            format_func=lambda x: (
                "min/km" if x == "km" else "min/mile"
            ),
            key="running_pace_unit",
        )

    # Calculate speed.
    try:
        speed_kmh, speed_mph = pace_to_speed(
            pace_minutes,
            pace_seconds,
            pace_unit,
        )
    except ValueError as e:
        st.error(str(e))
        return

    st.markdown("### Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric(
            "Speed",
            (
                f"{speed_kmh:.2f} km/h"
                if pace_unit == "km"
                else f"{speed_mph:.2f} mph"
            ),
        )

    with result_col2:
        st.metric(
            "Equivalent speed",
            (
                f"{speed_mph:.2f} mph"
                if pace_unit == "km"
                else f"{speed_kmh:.2f} km/h"
            ),
        )

    # Equivalent pace in the other unit.
    if pace_unit == "km":
        equivalent_pace = format_pace(60 / speed_mph)

        st.info(
            f"Equivalent pace: **{equivalent_pace} min/mile**"
        )

    else:
        equivalent_pace = format_pace(60 / speed_kmh)

        st.info(
            f"Equivalent pace: **{equivalent_pace} min/km**"
        )

    st.divider()

    # =====================================================
    # SECTION 2 — TARGET TIME TO PACE
    # =====================================================

    st.subheader("🎯 Distance + Target Time → Required Pace")

    st.write(
        "Choose a standard race distance or enter your own "
        "distance and target finishing time."
    )

    # -----------------------------------------------------
    # Distance
    # -----------------------------------------------------

    distance_type = st.selectbox(
        "Distance",
        list(STANDARD_DISTANCES.keys()) + ["Custom"],
        key="running_distance_type",
    )

    if distance_type == "Custom":

        col1, col2 = st.columns(2)

        with col1:
            distance = st.number_input(
                "Distance",
                min_value=0.01,
                value=10.0,
                step=0.1,
                format="%.2f",
                key="running_custom_distance",
            )

        with col2:
            distance_unit = st.selectbox(
                "Distance unit",
                ["km", "mile"],
                format_func=lambda x: (
                    "Kilometres (km)"
                    if x == "km"
                    else "Miles"
                ),
                key="running_distance_unit",
            )

    else:

        distance, distance_unit = STANDARD_DISTANCES[
            distance_type
        ]

        st.info(
            f"**{distance_type}:** "
            f"{distance:g} {distance_unit}"
        )

    # -----------------------------------------------------
    # Target time
    # -----------------------------------------------------

    st.markdown("### Target finishing time")

    col1, col2, col3 = st.columns(3)

    with col1:
        target_hours = st.number_input(
            "Hours",
            min_value=0,
            max_value=99,
            value=0,
            step=1,
            key="running_target_hours",
        )

    with col2:
        target_minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=50,
            step=1,
            key="running_target_minutes",
        )

    with col3:
        target_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            key="running_target_seconds",
        )

    # -----------------------------------------------------
    # Calculate
    # -----------------------------------------------------

    try:

        (
            pace_min_per_km,
            pace_min_per_mile,
            speed_kmh,
            speed_mph,
        ) = distance_and_time_to_pace(
            distance=distance,
            distance_unit=distance_unit,
            hours=target_hours,
            minutes=target_minutes,
            seconds=target_seconds,
        )

    except ValueError as e:

        st.error(str(e))
        return

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    st.markdown("### Required average")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric(
            "Pace",
            f"{format_pace(pace_min_per_km)} min/km",
        )

    with result_col2:
        st.metric(
            "Pace",
            f"{format_pace(pace_min_per_mile)} min/mile",
        )

    speed_col1, speed_col2 = st.columns(2)

    with speed_col1:
        st.metric(
            "Speed",
            f"{speed_kmh:.2f} km/h",
        )

    with speed_col2:
        st.metric(
            "Speed",
            f"{speed_mph:.2f} mph",
        )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    total_target_seconds = (
        target_hours * 3600
        + target_minutes * 60
        + target_seconds
    )

    target_time_display = (
        f"{total_target_seconds // 3600:02d}:"
        f"{(total_target_seconds % 3600) // 60:02d}:"
        f"{total_target_seconds % 60:02d}"
    )

    st.success(
        f"To complete **{distance:g} {distance_unit}** "
        f"in **{target_time_display}**, you need to average "
        f"**{format_pace(pace_min_per_km)} min/km** "
        f"({format_pace(pace_min_per_mile)} min/mile)."
    )

    st.caption(
        "Pace and speed are average values. Your actual pace "
        "may vary throughout the run."
    )
