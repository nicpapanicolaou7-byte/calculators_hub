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
# SESSION STATE
# =========================================================

if "selected_calculator" not in st.session_state:
    st.session_state.selected_calculator = "home"


# =========================================================
# SIDEBAR NAVIGATION
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


# Work out which option should be selected
option_keys = list(navigation_options.keys())

current_selection = st.session_state.selected_calculator

if current_selection not in option_keys:
    current_selection = "home"

default_index = option_keys.index(current_selection)


selected = st.sidebar.radio(
    "Navigation",
    options=option_keys,
    index=default_index,
    format_func=lambda key: navigation_options[key],
)

# Keep our own state synchronized with the sidebar
st.session_state.selected_calculator = selected


# =========================================================
# HOME PAGE
# =========================================================

if selected == "home":

    st.title("🧮 Calculator Hub")

    st.markdown(
        "Simple tools to help you calculate, compare, and plan."
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
    # Display categories
    # -----------------------------------------------------

    for category, calculators in categories.items():

        st.header(category)

        # Three calculator cards per row
        columns = st.columns(3)

        for index, (key, calculator) in enumerate(calculators):

            with columns[index % 3]:

                # Native Streamlit bordered container
                # instead of custom HTML
                with st.container(border=True):

                    st.markdown(
                        f"# {calculator['icon']}"
                    )

                    st.subheader(
                        calculator["name"]
                    )

                    st.write(
                        calculator["description"]
                    )

                    st.write("")

                    if st.button(
                        f"Open Calculator →",
                        key=f"open_{key}",
                        use_container_width=True,
                    ):

                        # Only change OUR session state.
                        # We don't modify the radio widget
                        # directly.
                        st.session_state.selected_calculator = key

                        st.rerun()


# =========================================================
# CALCULATOR PAGE
# =========================================================

else:

    calculator = CALCULATORS[selected]

    # Back to home button
    if st.button("← Back to Calculator Hub"):

        st.session_state.selected_calculator = "home"

        st.rerun()

    st.divider()

    # Render selected calculator
    calculator["render"]()
