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

def calculate_loan_payment_extra(
    loan_amount,
    years,
    annual_rate,
    payments_per_year=12,
    extra_annual_payment=0
):
    """
    Calculate loan repayment with an additional annual payment
    directly against the principal.

    Returns:
        monthly_payment: Normal monthly installment
        total_interest: Total interest paid with extra payments
        total_extra_paid: Total amount of extra payments made
        months: Number of months until the loan is fully repaid
    """

    # Convert annual interest rate to monthly
    monthly_interest_rate = annual_rate / 100 / 12

    # Calculate the normal monthly payment
    monthly_payment, _, _, _ = calculate_loan_payment(
        loan_amount,
        annual_rate,
        years,
        payments_per_year
    )

    # Simulate the loan month by month
    balance = loan_amount
    total_interest = 0
    total_extra_paid = 0
    months = 0

    schedule = []

    while balance > 0:
        months += 1

        # Calculate interest for this month
        interest = balance * monthly_interest_rate
        total_interest += interest

        # Calculate principal portion of normal payment
        principal = monthly_payment - interest

        # Make sure we don't overpay the balance
        principal = min(principal, balance)

        # Reduce the balance
        balance -= principal

        extra_payment = 0

        # Once a year, make the extra principal payment
        if months % 12 == 0 and balance > 0:
            extra_payment = min(extra_annual_payment, balance)
            balance -= extra_payment
            total_extra_paid += extra_payment

        # -----------------------------------------------------
        # Add row to schedule
        # -----------------------------------------------------

        schedule.append(
            {
                "Payment #": months,
                "Payment": monthly_payment,
                "Principal": principal,
                "Interest": interest,
                "Extra Payment": extra_payment,
                "Balance": max(
                    balance,
                    0,
                ),
            }
        )

        # Stop if loan is paid off
        if balance <= 0:
            break

    loan_paid_off_in = f"{months // 12} years and {months % 12} months"
    total_repayment = (
        loan_amount
        + total_interest
    )

    schedule = pd.DataFrame(
        schedule
    )

    return (
        monthly_payment,
        total_interest,
        total_repayment,
        loan_paid_off_in,
        schedule
    )


# =========================================================
# COMPOUND INTEREST
# =========================================================

import pandas as pd
from datetime import date, timedelta

import pandas as pd


def calculate_compound_interest(
    initial_investment,
    monthly_contribution,
    annual_rate,
    years,
    compounds_per_year=12,
):
    """
    Calculate compound investment growth with monthly contributions.

    Parameters
    ----------
    initial_investment : float
        Initial amount invested at the beginning.

    monthly_contribution : float
        Contribution made at the END of every month.

    annual_rate : float
        Nominal annual interest rate as a percentage.
        Example: 8 means 8%.

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
    final_balance : float
        Final investment value.

    total_contributions : float
        Total amount deposited.

    total_interest : float
        Final balance minus total contributions.

    yearly_data : pandas.DataFrame
        Year-by-year investment results.

    Notes
    -----
    Contributions occur at the END of each month.

    For annual, semi-annual, quarterly and monthly
    compounding, interest is applied only on the
    appropriate compounding month.

    Daily compounding is handled separately because
    365 days do not divide evenly into 12 calendar months.
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
    # Setup
    # ---------------------------------------------------------

    rate = annual_rate / 100

    total_months = years * 12

    balance = float(initial_investment)

    yearly_results = []

    # ---------------------------------------------------------
    # Annual / semi-annual / quarterly / monthly
    # ---------------------------------------------------------

    if compounds_per_year in {1, 2, 4, 12}:

        # Number of months between compounding events.
        months_per_compound = (
            12 // compounds_per_year
        )

        # Nominal rate per compounding period.
        periodic_rate = (
            rate / compounds_per_year
        )

        for month in range(1, total_months + 1):

            # Contribution at END of month.
            balance += monthly_contribution

            # Apply interest when a compounding period ends.
            if month % months_per_compound == 0:

                balance *= (
                    1 + periodic_rate
                )

            # Record at end of every year.
            if month % 12 == 0:

                year = month // 12

                total_contributions = (
                    initial_investment
                    + monthly_contribution * month
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
    # Daily compounding
    # ---------------------------------------------------------

    else:

        # For daily compounding, use a daily rate.
        daily_rate = rate / 365

        balance = float(initial_investment)

        # We need to know when each month ends.
        #
        # Rather than using calendar dates, we use the
        # standard financial assumption of 365 days/year
        # and distribute the 12 contributions across the year.
        #
        # Contribution months occur at:
        # 1/12, 2/12, ..., 12/12 of each year.

        days_per_month = 365 / 12

        next_contribution_month = 1

        for day in range(
            1,
            years * 365 + 1,
        ):

            # Daily compounding.
            balance *= (
                1 + daily_rate
            )

            # Determine which monthly contribution
            # should happen.
            current_month = int(
                day / days_per_month
            )

            if (
                current_month >=
                next_contribution_month
            ):

                balance += monthly_contribution

                next_contribution_month += 1

            # End of year.
            if day % 365 == 0:

                year = day // 365

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
    # Final totals
    # ---------------------------------------------------------

    total_contributions = (
        initial_investment
        + monthly_contribution
        * total_months
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
