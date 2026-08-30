import pandas as pd


# =========================================================
# LOAN CALCULATOR
# =========================================================

def calculate_loan_payment(
    principal,
    annual_rate,
    years,
    payments_per_year=12,
):
    """
    Calculate loan payment and amortization schedule.
    """

    number_of_payments = (
        years * payments_per_year
    )

    periodic_rate = (
        annual_rate
        / 100
        / payments_per_year
    )

    # Zero-interest loan
    if periodic_rate == 0:

        payment = (
            principal
            / number_of_payments
        )

    else:

        payment = (
            principal
            * periodic_rate
            * (1 + periodic_rate)
            ** number_of_payments
            /
            (
                (1 + periodic_rate)
                ** number_of_payments
                - 1
            )
        )

    balance = principal

    total_interest = 0

    schedule = []

    for period in range(
        1,
        number_of_payments + 1,
    ):

        interest = (
            balance
            * periodic_rate
        )

        principal_payment = (
            payment
            - interest
        )

        # Prevent the final payment from
        # exceeding the remaining balance.
        principal_payment = min(
            principal_payment,
            balance,
        )

        balance -= principal_payment

        total_interest += interest

        schedule.append(
            {
                "Payment #": period,
                "Payment": payment,
                "Principal": principal_payment,
                "Interest": interest,
                "Balance": max(
                    balance,
                    0,
                ),
            }
        )

    total_repayment = (
        principal
        + total_interest
    )

    schedule = pd.DataFrame(
        schedule
    )

    return (
        payment,
        total_interest,
        total_repayment,
        schedule,
    )


# =========================================================
# COMPOUND INTEREST
# =========================================================

import pandas as pd
from datetime import date, timedelta


def calculate_compound_interest(
    initial_investment,
    monthly_contribution,
    annual_rate,
    years,
    compounds_per_year=12,
):
    """
    Calculate investment growth with monthly contributions.

    Parameters
    ----------
    initial_investment : float
        Initial amount invested at the beginning.

    monthly_contribution : float
        Contribution made at the end of each calendar month.

    annual_rate : float
        Nominal annual interest rate as a percentage.
        Example: 10 means 10%.

    years : int
        Number of years.

    compounds_per_year : int
        Compounding frequency:

            1   = annually
            2   = semi-annually
            4   = quarterly
            12  = monthly
            365 = daily

    Returns
    -------
    tuple
        final_balance
        total_contributions
        total_interest
        yearly_data

    Notes
    -----
    - Contributions occur at the end of each calendar month.
    - Interest compounds according to compounds_per_year.
    - Daily compounding uses 365 days per year.
    - Leap years are handled naturally for contribution dates.
    """

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    if initial_investment < 0:
        raise ValueError(
            "initial_investment must be >= 0"
        )

    if monthly_contribution < 0:
        raise ValueError(
            "monthly_contribution must be >= 0"
        )

    if annual_rate < 0:
        raise ValueError(
            "annual_rate must be >= 0"
        )

    if not isinstance(years, int) or years <= 0:
        raise ValueError(
            "years must be a positive integer"
        )

    valid_frequencies = {
        1,
        2,
        4,
        12,
        365,
    }

    if compounds_per_year not in valid_frequencies:
        raise ValueError(
            "compounds_per_year must be "
            "1, 2, 4, 12, or 365"
        )

    # ---------------------------------------------------------
    # Basic setup
    # ---------------------------------------------------------

    rate = annual_rate / 100

    start_date = date.today()

    balance = float(initial_investment)

    yearly_results = []

    # Total number of days.
    end_date = date(
        start_date.year + years,
        start_date.month,
        start_date.day,
    )

    current_date = start_date

    # Track next monthly contribution.
    contribution_month = start_date.month
    contribution_year = start_date.year

    # ---------------------------------------------------------
    # Daily simulation
    # ---------------------------------------------------------

    while current_date < end_date:

        # -----------------------------------------------------
        # Determine whether interest compounds today
        # -----------------------------------------------------

        should_compound = False

        if compounds_per_year == 365:
            # Every day.
            should_compound = True

        elif compounds_per_year == 12:
            # End of each month.
            next_day = current_date + timedelta(days=1)

            should_compound = (
                next_day.month != current_date.month
            )

        elif compounds_per_year == 4:
            # End of Mar, Jun, Sep, Dec.
            next_day = current_date + timedelta(days=1)

            should_compound = (
                current_date.month in {3, 6, 9, 12}
                and next_day.month != current_date.month
            )

        elif compounds_per_year == 2:
            # End of Jun and Dec.
            next_day = current_date + timedelta(days=1)

            should_compound = (
                current_date.month in {6, 12}
                and next_day.month != current_date.month
            )

        elif compounds_per_year == 1:
            # End of December.
            next_day = current_date + timedelta(days=1)

            should_compound = (
                current_date.month == 12
                and next_day.month == 1
            )

        # -----------------------------------------------------
        # Apply interest
        # -----------------------------------------------------

        if should_compound:

            periodic_rate = (
                rate / compounds_per_year
            )

            balance *= (
                1 + periodic_rate
            )

        # -----------------------------------------------------
        # Monthly contribution
        #
        # Contribution happens at the END of the month.
        # -----------------------------------------------------

        next_day = current_date + timedelta(days=1)

        if next_day.month != current_date.month:

            balance += monthly_contribution

        # -----------------------------------------------------
        # Move to next day
        # -----------------------------------------------------

        current_date = next_day

        # -----------------------------------------------------
        # Record year-end result
        # -----------------------------------------------------

        if (
            current_date.month == 1
            and current_date.day == 1
        ):

            year = current_date.year - start_date.year

            total_contributions = (
                initial_investment
                + monthly_contribution
                * year
                * 12
            )

            interest_earned = (
                balance - total_contributions
            )

            yearly_results.append(
                {
                    "Year": year,
                    "Contributions": total_contributions,
                    "Interest": interest_earned,
                    "Balance": balance,
                }
            )

    # ---------------------------------------------------------
    # Final values
    # ---------------------------------------------------------

    total_contributions = (
        initial_investment
        + monthly_contribution
        * years
        * 12
    )

    interest_earned = (
        balance - total_contributions
    )

    yearly_data = pd.DataFrame(
        yearly_results
    )

    return (
        balance,
        total_contributions,
        interest_earned,
        yearly_data,
    )
def calculate_compound_interest2(
    initial_investment,
    monthly_contribution,
    annual_rate,
    years,
    compounds_per_year=12,
):
    """
    Calculate investment growth with
    regular monthly contributions.
    """

    total_months = years * 12

    annual_rate_decimal = (
        annual_rate / 100
    )

    # Convert annual rate to an effective
    # monthly rate based on compounding frequency.
    if annual_rate_decimal == 0:

        monthly_rate = 0

    else:

        periodic_rate = (
            (1 + annual_rate_decimal)
            ** (1 / compounds_per_year)
            - 1
        )

        monthly_rate = (
            (1 + periodic_rate)
            ** (compounds_per_year / 12)
            - 1
        )

    balance = initial_investment

    yearly_results = []

    for month in range(
        1,
        total_months + 1,
    ):

        # Interest earned during the month
        interest = (
            balance
            * monthly_rate
        )

        balance += interest

        # Monthly contribution
        balance += monthly_contribution

        # Record once per year
        if month % 12 == 0:

            year = month // 12

            total_contributions = (
                initial_investment
                + monthly_contribution
                * month
            )

            interest_earned = (
                balance
                - total_contributions
            )

            yearly_results.append(
                {
                    "Year": year,
                    "Contributions": total_contributions,
                    "Interest": interest_earned,
                    "Balance": balance,
                }
            )

    total_contributions = (
        initial_investment
        + monthly_contribution
        * total_months
    )

    interest_earned = (
        balance
        - total_contributions
    )

    yearly_data = pd.DataFrame(
        yearly_results
    )

    return (
        balance,
        total_contributions,
        interest_earned,
        yearly_data,
    )
