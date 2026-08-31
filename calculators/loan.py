import streamlit as st
import pandas as pd

from utils.calculations import calculate_loan_payment, calculate_loan_payment_extra


def render_loan_calculator():

    st.markdown(
        '<div class="main-title">🏠 Loan Calculator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Calculate your payment, total interest, "
        "and repayment schedule."
        "</div>",
        unsafe_allow_html=True,
    )

    # =====================================================
    # INPUTS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        loan_amount = st.number_input(
            "Loan amount",
            min_value=0.0,
            value=250_000.0,
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

        extra_annual_payment = st.number_input(
            "Extra Annual Payment",
            min_value=0,
            value=0,
            step=100,
            format="%.2f",
            help=(
                    "Additional amount paid directly towards "
                    "the principal once every year."
                ),
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
            "Payment frequency",
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

    # =====================================================
    # CALCULATION
    # =====================================================

    (
        payment,
        total_interest,
        total_repayment,
        schedule,
    ) = calculate_loan_payment(
        principal=loan_amount,
        annual_rate=interest_rate,
        years=loan_term_years,
        payments_per_year=payments_per_year,
    )

    if extra_annual_payment > 0:
    
        (
            extra_payment,
            extra_total_interest,
            extra_total_repayment,
            loan_paid_off_in,
            extra_schedule,
        ) = calculate_loan_payment_extra(
            loan_amount=loan_amount,
            years=loan_term_years,
            annual_rate=interest_rate,
            payments_per_year=payments_per_year,
            extra_annual_payment=extra_annual_payment,
        )
    
    else:
    
        extra_payment = 0.0
        extra_total_interest = None
        extra_total_repayment = None    
        loan_paid_off_in = f"{loan_term_years} years"
        extra_schedule = None

    # =====================================================
    # RESULTS
    # =====================================================

    st.subheader("Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Payment",
            f"€{payment:,.2f}",
        )

    with col2:
        st.metric(
            "Total interest",
            f"€{total_interest:,.2f}",
        )

    with col3:
        st.metric(
            "Total repayment",
            f"€{total_repayment:,.2f}",
        )

    with col4:
        st.metric(
            "Loan paid in",
            f"{loan_paid_off_in}",
        )

    st.divider()

    # =====================================================
    # PAYMENT BREAKDOWN
    # =====================================================

    st.subheader("Payment breakdown")

    chart_data = pd.DataFrame(
        {
            "Amount": [
                loan_amount,
                total_interest,
            ]
        },
        index=[
            "Principal",
            "Interest",
        ],
    )

    st.bar_chart(chart_data)

    # =====================================================
    # AMORTIZATION
    # =====================================================

    st.subheader("Amortization schedule")

    display_schedule = schedule.copy()

    for column in [
        "Payment",
        "Principal",
        "Interest",
        "Balance",
    ]:

        display_schedule[column] = (
            display_schedule[column]
            .map(lambda x: f"€{x:,.2f}")
        )

    st.dataframe(
        display_schedule,
        use_container_width=True,
        hide_index=True,
    )

    if extra_schedule is not None:

        st.divider()
    
        st.subheader(
            "Amortization schedule with extra payments"
        )
    
        display_extra_schedule = extra_schedule.copy()
    
        for column in [
            "Payment",
            "Principal",
            "Interest",
            "Extra Payment",
            "Balance",
        ]:
    
            display_extra_schedule[column] = (
                display_extra_schedule[column]
                .map(lambda x: f"€{x:,.2f}")
            )
    
        st.dataframe(
            display_extra_schedule,
            use_container_width=True,
            hide_index=True,
        )
