```python
import streamlit as st
import pandas as pd

from utils.calculations import calculate_compound_interest


def render_compound_interest_calculator():

    st.markdown(
        '<div class="main-title">📈 Compound Interest Calculator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        'See how your money can grow through compound interest and regular contributions.'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Inputs
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        initial_investment = st.number_input(
            "Initial investment",
            min_value=0.0,
            value=10000.0,
            step=500.0,
            format="%.2f",
        )

        monthly_contribution = st.number_input(
            "Monthly contribution",
            min_value=0.0,
            value=500.0,
            step=50.0,
            format="%.2f",
        )

        annual_return = st.number_input(
            "Annual interest / return (%)",
            min_value=0.0,
            max_value=100.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )

    with col2:

        years = st.number_input(
            "Investment period (years)",
            min_value=1,
            max_value=100,
            value=20,
            step=1,
        )

        compounding = st.selectbox(
            "Compounding frequency",
            options=[1, 2, 4, 12, 365],
            index=3,
            format_func=lambda x: {
                1: "Annually",
                2: "Semi-annually",
                4: "Quarterly",
                12: "Monthly",
                365: "Daily",
            }[x],
        )

    st.divider()

    # -----------------------------------------------------
    # Calculate
    # -----------------------------------------------------

    final_balance, total_contributions, interest_earned, yearly_data = (
        calculate_compound_interest(
            initial_investment=initial_investment,
            monthly_contribution=monthly_contribution,
            annual_rate=annual_return,
            years=years,
            compounds_per_year=compounding,
        )
    )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    st.subheader("Results")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric(
            "Final balance",
            f"€{final_balance:,.2f}",
        )

    with result_col2:
        st.metric(
            "Total contributions",
            f"€{total_contributions:,.2f}",
        )

    with result_col3:
        st.metric(
            "Interest earned",
            f"€{interest_earned:,.2f}",
        )

    st.divider()

    # -----------------------------------------------------
    # Growth chart
    # -----------------------------------------------------

    st.subheader("Investment growth")

    chart_data = yearly_data.set_index("Year")[
        ["Contributions", "Interest", "Balance"]
    ]

    st.line_chart(chart_data)

    # -----------------------------------------------------
    # Year-by-year table
    # -----------------------------------------------------

    st.subheader("Year-by-year breakdown")

    display_data = yearly_data.copy()

    for column in ["Contributions", "Interest", "Balance"]:
        display_data[column] = display_data[column].map(
            lambda x: f"€{x:,.2f}"
        )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )
```
