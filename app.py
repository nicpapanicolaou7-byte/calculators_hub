import streamlit as st

from calculators.registry import CALCULATORS


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Calculator Hub",
    page_icon="🧮",
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

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
        margin-bottom: 0.5rem;
        min-height: 190px;
    }

    .calculator-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .calculator-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .calculator-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "selected_calculator" not in st.session_state:
    st.session_state.selected_calculator = "home"


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧮 Calculator Hub")

st.sidebar.caption("Choose a calculator")

navigation_options = {
    "home": "🏠 Calculator Home",
}

for key, calculator in CALCULATORS.items():

    navigation_options[key] = (
        f"{calculator['icon']} {calculator['name']}"
    )


selected = st.sidebar.radio(
    "Navigation",
    options=list(navigation_options.keys()),
    format_func=lambda key: navigation_options[key],
    key="navigation",
)


# Keep session state synchronized with sidebar
st.session_state.selected_calculator = selected


# =========================================================
# HOME PAGE
# =========================================================

if selected == "home":

    st.markdown(
        '<div class="main-title">🧮 Calculator Hub</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Simple tools to help you calculate, compare, and plan."
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # -----------------------------------------------------
    # Group calculators by category
    # -----------------------------------------------------

    categories = {}

    for key, calculator in CALCULATORS.items():

        category = calculator.get(
            "category",
            "Other",
        )

        if category not in categories:
            categories[category] = []

        categories[category].append(
            (key, calculator)
        )

    # -----------------------------------------------------
    # Display calculator categories
    # -----------------------------------------------------

    for category, calculators in categories.items():

        st.subheader(category)

        columns = st.columns(3)

        for index, (key, calculator) in enumerate(calculators):

            with columns[index % 3]:

                st.markdown(
                    f"""
                    <div class="calculator-card">

                        <div class="calculator-icon">
                            {calculator['icon']}
                        </div>

                        <div class="calculator-title">
                            {calculator['name']}
                        </div>

                        <div class="calculator-description">
                            {calculator['description']}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # -------------------------------------------------
                # Open calculator button
                # -------------------------------------------------

                if st.button(
                    f"Open {calculator['name']} →",
                    key=f"open_{key}",
                    use_container_width=True,
                ):

                    st.session_state.navigation = key
                    st.session_state.selected_calculator = key

                    st.rerun()


# =========================================================
# CALCULATOR PAGE
# =========================================================

else:

    calculator = CALCULATORS[selected]

    calculator["render"]()
