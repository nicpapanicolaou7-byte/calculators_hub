```python
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
```
