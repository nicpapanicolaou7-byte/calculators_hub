```python
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cpi_data.csv"
)


CURRENCY_INFO = {
    "USD": {
        "name": "US Dollar",
        "symbol": "$",
        "index_name": "U.S. CPI-U",
        "country": "United States",
        "minimum_year": 1913,
        "note": (
            "U.S. CPI-U, all items, U.S. city average. "
            "The latest 2026 value is the August 2026 monthly index, "
            "not an annual average."
        ),
    },
    "GBP": {
        "name": "British Pound",
        "symbol": "£",
        "index_name": "UK CPI",
        "country": "United Kingdom",
        "minimum_year": 1988,
        "note": (
            "UK Consumer Prices Index (CPI), all items. "
            "The official CPI series begins in 1988. "
            "The latest 2026 value is the August 2026 monthly index, "
            "not an annual average."
        ),
    },
    "EUR": {
        "name": "Euro",
        "symbol": "€",
        "index_name": "Euro Area HICP",
        "country": "Euro area",
        "minimum_year": 2002,
        "note": (
            "Euro-area Harmonised Index of Consumer Prices (HICP), "
            "all items. The calculator starts EUR calculations in 2002, "
            "when euro banknotes and coins entered circulation. "
            "The latest 2026 value is the August 2026 monthly index, "
            "not an annual average."
        ),
    },
}


# =========================================================
# LOAD CPI DATA
# =========================================================

@st.cache_data
def load_cpi_data():
    """
    Load CPI data from the CSV file.
    """

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"CPI data file not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = {
        "currency",
        "country_or_area",
        "year",
        "index",
        "index_type",
        "index_reference",
        "minimum_year",
        "note",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "The CPI CSV is missing the following columns: "
            + ", ".join(sorted(missing_columns))
        )

    df["year"] = df["year"].astype(int)
    df["index"] = df["index"].astype(float)

    return df


# =========================================================
# GET AVAILABLE YEARS
# =========================================================

def get_currency_data(df, currency):
    """
    Return CPI data for a specific currency.
    """

    currency_data = df[
        df["currency"] == currency
    ].copy()

    if currency_data.empty:
        raise ValueError(
            f"No CPI data available for {currency}."
        )

    currency_data = currency_data.sort_values("year")

    return currency_data


# =========================================================
# CALCULATION
# =========================================================

def calculate_historical_value(
    amount,
    from_year,
    to_year,
    currency_data,
):
    """
    Calculate the purchasing-power equivalent of an amount
    from one year to another.

    Formula:

        Target Value =
            Original Value ×
            (Target CPI / Original CPI)

    """

    from_rows = currency_data[
        currency_data["year"] == from_year
    ]

    to_rows = currency_data[
        currency_data["year"] == to_year
    ]

    if from_rows.empty:
        raise ValueError(
            f"No CPI data is available for {from_year}."
        )

    if to_rows.empty:
        raise ValueError(
            f"No CPI data is available for {to_year}."
        )

    from_index = float(
        from_rows.iloc[0]["index"]
    )

    to_index = float(
        to_rows.iloc[0]["index"]
    )

    result = amount * (to_index / from_index)

    return result, from_index, to_index


# =========================================================
# FORMAT CURRENCY
# =========================================================

def format_money(value, symbol):
    """
    Format a monetary value nicely.
    """

    return f"{symbol}{value:,.2f}"


# =========================================================
# RENDER CALCULATOR
# =========================================================

def render_historical_money_value_calculator():

    # -----------------------------------------------------
    # Load data
    # -----------------------------------------------------

    try:
        df = load_cpi_data()

    except Exception as error:
        st.error(
            "Unable to load the CPI data."
        )

        st.exception(error)

        return

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    st.title(
        "💰 Historical Money Value"
    )

    st.markdown(
        """
        Find out how much money from one year would be worth
        in another year based on changes in consumer prices.
        """
    )

    st.info(
        """
        This calculator measures changes in purchasing power
        using consumer price indices. It does **not** represent
        investment returns, interest, exchange rates, wages,
        house prices, or the value of a specific asset.
        """
    )

    # -----------------------------------------------------
    # Currency selection
    # -----------------------------------------------------

    currency = st.selectbox(
        "Currency",
        options=list(CURRENCY_INFO.keys()),
        format_func=lambda x: (
            f"{x} — {CURRENCY_INFO[x]['name']}"
        ),
    )

    info = CURRENCY_INFO[currency]

    # -----------------------------------------------------
    # Currency information
    # -----------------------------------------------------

    st.caption(
        f"Index used: **{info['index_name']}**"
    )

    # -----------------------------------------------------
    # Filter data for selected currency
    # -----------------------------------------------------

    try:
        currency_data = get_currency_data(
            df,
            currency,
        )

    except ValueError as error:
        st.error(str(error))
        return

    # -----------------------------------------------------
    # Available years
    # -----------------------------------------------------

    available_years = sorted(
        currency_data["year"].unique()
    )

    minimum_year = info["minimum_year"]
    maximum_year = max(available_years)

    available_years = [
        year
        for year in available_years
        if year >= minimum_year
    ]

    # -----------------------------------------------------
    # Inputs
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            value=1000.00,
            step=100.00,
            format="%.2f",
        )

    with col2:

        from_year = st.selectbox(
            "From year",
            options=available_years,
            index=(
                available_years.index(1960)
                if 1960 in available_years
                else 0
            ),
        )

    to_year = st.selectbox(
        "To year",
        options=available_years,
        index=len(available_years) - 1,
    )

    # -----------------------------------------------------
    # Currency-specific note
    # -----------------------------------------------------

    if currency == "EUR":

        st.caption(
            "ℹ️ EUR calculations start at 2002 because "
            "euro banknotes and coins entered circulation "
            "in 2002. Euro-area HICP data exist for earlier "
            "periods, but those years are intentionally "
            "not selectable in this calculator."
        )

    elif currency == "GBP":

        st.caption(
            "ℹ️ UK CPI calculations start at 1988, "
            "the beginning of the official CPI series."
        )

    elif currency == "USD":

        st.caption(
            "ℹ️ U.S. CPI-U data are available from 1913."
        )

    # -----------------------------------------------------
    # Calculate
    # -----------------------------------------------------

    if st.button(
        "Calculate",
        type="primary",
        use_container_width=True,
    ):

        try:

            (
                equivalent_value,
                from_index,
                to_index,
            ) = calculate_historical_value(
                amount=amount,
                from_year=from_year,
                to_year=to_year,
                currency_data=currency_data,
            )

        except ValueError as error:

            st.error(str(error))

            return

        # -------------------------------------------------
        # Results
        # -------------------------------------------------

        st.divider()

        st.subheader("Result")

        symbol = info["symbol"]

        formatted_original = format_money(
            amount,
            symbol,
        )

        formatted_result = format_money(
            equivalent_value,
            symbol,
        )

        st.metric(
            label=(
                f"Equivalent purchasing power in "
                f"{to_year}"
            ),
            value=formatted_result,
        )

        st.markdown(
            f"""
            **{formatted_original} in {from_year}**
            had approximately the same purchasing power as

            # {formatted_result}

            in **{to_year}**.
            """
        )

        # -------------------------------------------------
        # Change calculations
        # -------------------------------------------------

        percentage_change = (
            (equivalent_value / amount) - 1
        ) * 100

        multiplier = (
            equivalent_value / amount
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Purchasing-power change",
                f"{percentage_change:,.1f}%",
            )

        with col2:

            st.metric(
                "Value multiplier",
                f"{multiplier:,.2f}×",
            )

        # -------------------------------------------------
        # CPI information
        # -------------------------------------------------

        st.divider()

        st.subheader(
            "How the calculation works"
        )

        st.write(
            f"The {info['index_name']} was "
            f"**{from_index:,.3f}** in {from_year} "
            f"and **{to_index:,.3f}** in {to_year}."
        )

        st.code(
            f"{formatted_original} × "
            f"({to_index:,.3f} ÷ {from_index:,.3f}) "
            f"= {formatted_result}"
        )

        # -------------------------------------------------
        # Data note
        # -------------------------------------------------

        if to_year == maximum_year:

            st.warning(
                f"The {maximum_year} value is the latest "
                f"available monthly CPI/HICP observation "
                f"({maximum_year}-08 / August), not a "
                f"full-year average."
            )

        st.caption(
            info["note"]
        )

        st.caption(
            "Historical CPI values can be revised by the "
            "statistical agencies that publish them. "
            "Results should therefore be considered "
            "approximate purchasing-power comparisons."
        )


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":
    render_historical_money_value_calculator()
```
