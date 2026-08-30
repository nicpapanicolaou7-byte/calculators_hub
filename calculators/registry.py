from calculators.loan import render_loan_calculator
from calculators.compound_interest import (
    render_compound_interest_calculator,
)


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

}
