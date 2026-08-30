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

def calculate_compound_interest(
    initial_investment,
    monthly_contribution,
    annual_rate,
    years,
    compounds_per_year=12,
):
    """
    Calculate investment growth with regular monthly contributions.

    Parameters
    ----------
    initial_investment : float
        Amount invested at the beginning of the investment period.

    monthly_contribution : float
        Amount contributed at the END of each month.

    annual_rate : float
        Nominal annual interest rate expressed as a percentage.
        Example: 7.5 means 7.5%.

    years : int
        Number of years to invest.

    compounds_per_year : int, optional
        Number of times interest is compounded per year.

        Supported values:
            1   = annually
            2   = semi-annually
            4   = quarterly
            12  = monthly
            365 = daily

    Returns
    -------
    tuple
        (
            final_balance,
            total_contributions,
            total_interest,
            yearly_data
        )

        yearly_data is a pandas DataFrame containing:
            Year
            Contributions
            Interest
            Balance

    Notes
    -----
    - Contributions are made at the END of each month.
    - Interest is applied at each compounding period.
    - The initial investment is present from the beginning.
    - annual_rate is a nominal annual rate.
    - Daily compounding assumes 365 days per year.
    """

    # ---------------------------------------------------------
    # Validate inputs
    # ---------------------------------------------------------

    if initial_investment < 0:
        raise ValueError(
            "initial_investment must be >= 0."
        )

    if monthly_contribution < 0:
        raise ValueError(
            "monthly_contribution must be >= 0."
        )

    if annual_rate < 0:
        raise ValueError(
            "annual_rate must be >= 0."
        )

    if not isinstance(years, int):
        raise TypeError(
            "years must be an integer."
        )

    if years <= 0:
        raise ValueError(
            "years must be > 0."
        )

    valid_compounding = {
        1,
        2,
        4,
        12,
        365,
    }

    if compounds_per_year not in valid_compounding:
        raise ValueError(
            "compounds_per_year must be one of: "
            "1, 2, 4, 12, or 365."
        )

    # ---------------------------------------------------------
    # Setup
    # ---------------------------------------------------------

    annual_rate_decimal = annual_rate / 100

    # Rate applied at each compounding event.
    periodic_rate = (
        annual_rate_decimal / compounds_per_year
    )

    balance = float(initial_investment)

    yearly_results = []

    # ---------------------------------------------------------
    # Daily simulation
    # ---------------------------------------------------------

    total_days = years * 365

    for day in range(1, total_days + 1):

        # -----------------------------------------------------
        # Determine whether today is a monthly contribution day.
        #
        # Using 365 / 12 gives approximately 30.42 days/month.
        # Instead of pretending every month has the same number
        # of days, use the cumulative-month approach below.
        # -----------------------------------------------------

        current_month = int(
            (day - 1) * 12 / 365
        ) + 1

        previous_month = int(
            (day - 2) * 12 / 365
        ) + 1 if day > 1 else 0

        is_month_end = (
            current_month != previous_month
        )

        # -----------------------------------------------------
        # Apply interest
        # -----------------------------------------------------

        if day % (365 // compounds_per_year) == 0:
            balance *= (1 + periodic_rate)

        # -----------------------------------------------------
        # Add monthly contribution
        # -----------------------------------------------------

        if is_month_end:
            balance += monthly_contribution

        # -----------------------------------------------------
        # Record yearly results
        # -----------------------------------------------------

        if day % 365 == 0:

            year = day // 365

            total_months = year * 12

            total_contributions = (
                initial_investment
                + monthly_contribution * total_months
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
    # Final totals
    # ---------------------------------------------------------

    total_contributions = (
        initial_investment
        + monthly_contribution * years * 12
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
