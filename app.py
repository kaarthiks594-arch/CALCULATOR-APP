import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="MTE Calculator", layout="centered")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "ken_number" not in st.session_state:
    st.session_state.ken_number = ""
if "selected_modules" not in st.session_state:
    st.session_state.selected_modules = []
if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []
if "results" not in st.session_state:
    st.session_state.results = {}
if "show_details" not in st.session_state:
    st.session_state.show_details = {}

# ---------- MODULES & ACTIONS ----------
MODULES = [
    "Machines",
    "Ropes and Compensation",
    "Counterweights",
    "Electrification",
    "Drive Systems",
    "Shaft Equipments",
    "Guide Shoe",
    "Peripheral Devices",
    "Car",
    "Car Slings",
    "Door and Facings"
]

REPLACEMENT_ACTIONS = [
    "Replace Component A",
    "Replace Component B",
    "Replace Component C",
    "Repair Module",
    "Upgrade System",
    "Install New Part",
    "Remove Old Part",
    "Test and Verify",
]

# ---------- HEADER ----------
st.markdown(
    """
    <div style='background:#2563eb;padding:15px;border-radius:10px'>
    <h2 style='color:white;text-align:center'>MTE Calculator</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- HOME PAGE ----------
if st.session_state.page == "home":
    st.subheader("Choose how you want to proceed")
    if st.button("Search by KEN"):
        st.session_state.page = "ken_search"
        st.rerun()
    if st.button("Browse Modules"):
        st.session_state.page = "module_browser"
        st.session_state.ken_number = ""  # Clear KEN so Electrification does not appear
        st.rerun()

# ---------- KEN SEARCH ----------
elif st.session_state.page == "ken_search":
    st.subheader("KEN Search")
    ken = st.text_input("Enter KEN Number")
    if st.button("Search"):
        if ken.strip():
            st.session_state.ken_number = ken
            st.session_state.page = "module_browser"
            st.rerun()
        else:
            st.error("Please enter a KEN number")
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------- MODULE BROWSER ----------
elif st.session_state.page == "module_browser":

    # ---------- ELECTRIFICATION ----------
    if st.session_state.ken_number.strip():
        st.subheader("Electrification")
        st.info("LCS")

    # ---------- MODULE GRID (3-Column Layout) ----------
    st.subheader("Modules")
    cols = st.columns(3)
    for i, module in enumerate(MODULES):
        col = cols[i % 3]
        selected = module in st.session_state.selected_modules
        button_label = f"✅ {module}" if selected else module
        if col.button(button_label, key=f"mod_{module}"):
            if selected:
                st.session_state.selected_modules.remove(module)
            else:
                st.session_state.selected_modules.append(module)

    # Show selected modules below grid
    if st.session_state.selected_modules:
        st.markdown("**Selected Modules:**")
        for m in st.session_state.selected_modules:
            st.text(f"- {m}")

    # ---------- REPLACEMENT ACTIONS ----------
    st.subheader("Replacement Actions")
    if st.session_state.selected_modules:
        options = [f"{a} - {m}" for m in st.session_state.selected_modules for a in REPLACEMENT_ACTIONS]
        st.session_state.selected_actions = st.multiselect("Select replacement actions", options)
    else:
        st.warning("Select at least one module first")

    # ---------- CALCULATE MTE ----------
    if st.button("Calculate MTE"):
        if not st.session_state.selected_modules:
            st.error("Select at least one module")
        elif not st.session_state.selected_actions:
            st.error("Select at least one action")
        else:
            st.session_state.results = {}
            for action in st.session_state.selected_actions:
                st.session_state.results[action] = {
                    "time": "4.5",
                    "manpower": "3",
                    "prep": "1",
                    "replace": "2.5",
                    "final": "1"
                }
            # Overall MTE
            total_time = sum(float(v["time"]) for k, v in st.session_state.results.items())
            st.session_state.results["overall"] = f"{total_time}"
            st.success("MTE Calculated")

    if st.button("Back to Home"):
        st.session_state.selected_modules = []
        st.session_state.selected_actions = []
        st.session_state.results = {}
        st.session_state.page = "home"
        st.rerun()

    # ---------- RESULTS (VERTICAL MOBILE-FRIENDLY CARDS) ----------
    if st.session_state.results:
        st.write("---")
        st.subheader("Result")
        for action_name, values in st.session_state.results.items():
            if action_name == "overall":
                continue
            with st.expander(f"{action_name}"):
                st.write(f"**Time:** {values['time']}")
                st.write(f"**Manpower:** {values['manpower']}")
                with st.expander("Time Split"):
                    st.write(f"1. Preparation : {values['prep']}")
                    st.write(f"2. Replacement : {values['replace']}")
                    st.write(f"3. Finalisation : {values['final']}")
        # Overall MTE
        st.write("---")
        st.write("**Overall MTE:**")
        st.text(st.session_state.results["overall"])
