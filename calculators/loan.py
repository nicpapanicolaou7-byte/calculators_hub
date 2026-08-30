```python
import streamlit as st
import pandas as pd

from utils.calculations import calculate_loan_payment


def render_loan_calculator():

    st.markdown(
        '<div class="main-title">🏠 Loan Calculator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        'Calculate your monthly payment, total interest, and repayment schedule.'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Inputs
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input(
            "Loan amount",
            min_value=0.0,
            value=250000.0,
            step=5000.0,
            format="%.2f",
        )

        interest_rate = st.number_input(
            "Annual interest rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=4.5,
            step=0.1,
            format="%.2f",
        )

    with col2:
        loan_term_years = st.number_input(
            "Loan term (years)",
            min_value=1,
            max_value=50,
            value=25,
            step=1,
        )

        payments_per_year = st.selectbox(
            "Payments per year",
            options=[12, 4, 2, 1],
            index=0,
            format_func=lambda x: {
                12: "Monthly",
                4: "Quarterly",
                2: "Semi-annually",
                1: "Annually",
            }[x],
        )

    st.divider()

    # -----------------------------------------------------
    # Calculate
    # -----------------------------------------------------

    payment, total_interest, total_repayment, schedule = (
        calculate_loan_payment(
            principal=loan_amount,
            annual_rate=interest_rate,
            years=loan_term_years,
            payments_per_year=payments_per_year,
        )
    )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    st.subheader("Results")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric(
            "Payment",
            f"€{payment:,.2f}",
        )

    with result_col2:
        st.metric(
            "Total interest",
            f"€{total_interest:,.2f}",
        )

    with result_col3:
        st.metric(
            "Total repayment",
            f"€{total_repayment:,.2f}",
        )

    st.divider()

    # -----------------------------------------------------
    # Chart
    # -----------------------------------------------------

    st.subheader("Payment breakdown")

    chart_data = pd.DataFrame(
        {
            "Principal": [loan_amount],
            "Interest": [total_interest],
        }
    )

    st.bar_chart(chart_data)

    # -----------------------------------------------------
    # Amortization schedule
    # -----------------------------------------------------

    st.subheader("Amortization schedule")

    display_schedule = schedule.copy()

    for column in ["Payment", "Principal", "Interest", "Balance"]:
        display_schedule[column] = display_schedule[column].map(
            lambda x: f"€{x:,.2f}"
        )

    st.dataframe(
        display_schedule,
        use_container_width=True,
        hide_index=True,
    )
```
