import streamlit as st

st.set_page_config(page_title="MTE Calculator", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_modules" not in st.session_state:
    st.session_state.selected_modules = []

if "replacement_actions" not in st.session_state:
    st.session_state.replacement_actions = {}

# ---------------- DATA ----------------
modules = [
    "Brake System",
    "Traction Motor",
    "Pantograph",
    "Compressor",
    "Transformer",
    "Cooling System",
    "Control Electronics",
]

replacement_actions = {
    "Brake System": [
        "Replace Brake Pad",
        "Adjust Brake Cylinder",
        "Inspect Brake Pipe",
    ],
    "Traction Motor": [
        "Motor Overhaul",
        "Bearing Replacement",
        "Rotor Inspection",
    ],
    "Pantograph": [
        "Carbon Strip Replacement",
        "Spring Adjustment",
        "Arm Inspection",
    ],
    "Compressor": [
        "Compressor Seal Replacement",
        "Air Filter Change",
        "Valve Inspection",
    ],
    "Transformer": [
        "Oil Replacement",
        "Cooling Fan Check",
        "Insulation Test",
    ],
    "Cooling System": [
        "Coolant Replacement",
        "Pump Inspection",
        "Radiator Cleaning",
    ],
    "Control Electronics": [
        "PCB Replacement",
        "Firmware Update",
        "Connector Inspection",
    ],
}

# ---------------- HEADER ----------------
st.title("MTE Calculator")

# =================================================
# HOME PAGE
# =================================================
if st.session_state.page == "home":

    mode = st.radio(
        "Choose how you want to proceed",
        ["Search by KEN", "Browse Modules"],
        horizontal=True
    )

    # ---------------- KEN SEARCH ----------------
    if mode == "Search by KEN":

        ken = st.text_input("Enter KEN Number")

        if st.button("Search"):

            if ken.strip() == "":
                st.error("Please enter a KEN number")
            else:
                st.session_state.ken = ken
                st.session_state.page = "modules"
                st.rerun()

    # ---------------- DIRECT MODULE BROWSE ----------------
    else:

        if st.button("Open Modules"):
            st.session_state.page = "modules"
            st.rerun()

# =================================================
# MODULE PAGE
# =================================================
elif st.session_state.page == "modules":

    st.subheader("Select Modules")

    selected = st.multiselect(
        "Choose modules",
        modules,
        default=st.session_state.selected_modules
    )

    st.session_state.selected_modules = selected

    st.divider()

    # ---------------- SHOW SELECTED MODULES ----------------
    if selected:

        st.subheader("Selected Modules")

        for module in selected:

            st.markdown(f"### {module}")

            action = st.selectbox(
                f"Replacement Action for {module}",
                replacement_actions[module],
                key=f"action_{module}"
            )

            st.session_state.replacement_actions[module] = action

    else:
        st.info("Select modules to see replacement actions.")

    st.divider()

    # ---------------- SUMMARY ----------------
    if st.session_state.replacement_actions:

        st.subheader("Selected Replacement Actions")

        for module, action in st.session_state.replacement_actions.items():
            st.write(f"**{module}** → {action}")

    st.divider()

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
