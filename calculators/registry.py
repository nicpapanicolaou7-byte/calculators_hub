from calculators.loan import render_loan_calculator
from calculators.compound_interest import (
    render_compound_interest_calculator,
)
from calculators.historical_money_value import (
    render_historical_money_value_calculator,
)
from calculators.running_pace import render_running_pace_calculator


# =========================================================
# CALCULATOR REGISTRY
# =========================================================
#
# To add a new calculator:
#
# 1. Create a new file inside calculators/
# 2. Create a render_<calculator_name>_calculator() function
# 3. Import that function here
# 4. Add the calculator to CALCULATORS
#
# You do NOT need to modify app.py.
# =========================================================


CALCULATORS = {

    "loan": {
        "name": "Loan Calculator",
        "icon": "🏠",
        "category": "Finance",
        "description": (
            "Calculate monthly payments, "
            "total interest, and repayment."
        ),
        "render": render_loan_calculator,
    },

    "compound_interest": {
        "name": "Compound Interest",
        "icon": "📈",
        "category": "Investing",
        "description": (
            "Calculate how your money can grow "
            "with compound interest and regular contributions."
        ),
        "render": render_compound_interest_calculator,
    },

    "historical_money_value": {
        "name": "Historical Money Value",
        "icon": "💰",
        "category": "Finance",
        "description": (
            "See what money from one year would be worth "
            "in another year based on inflation."
        ),
        "render": render_historical_money_value_calculator,
    },

    "running_pace": {
        "name": "Running Pace & Speed",
        "icon": "🏃",
        "category": "Running & Fitness",
        "description": (
            "Convert running pace to speed and calculate "
            "the pace needed for a target finishing time."
        ),
        "render": render_running_pace_calculator,
    },

}
