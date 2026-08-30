```python
import streamlit as st

from calculators.loan import render_loan_calculator
from calculators.compound_interest import render_compound_interest_calculator


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Calculator Hub",
    page_icon="🧮",
    layout="wide",
)


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .subtitle {
            font-size: 1.15rem;
            color: #666;
            margin-bottom: 2rem;
        }

        .calculator-card {
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------

st.sidebar.title("🧮 Calculator Hub")

calculator = st.sidebar.radio(
    "Choose a calculator",
    [
        "🏠 Loan Calculator",
        "📈 Compound Interest Calculator",
    ],
)


# ---------------------------------------------------------
# Home / calculator selection
# ---------------------------------------------------------

if calculator == "🏠 Loan Calculator":
    render_loan_calculator()

elif calculator == "📈 Compound Interest Calculator":
    render_compound_interest_calculator()
```
