import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="MTE Calculator", layout="centered")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "ken_number" not in st.session_state:
    st.session_state.ken_number = ""

if "electrification" not in st.session_state:
    st.session_state.electrification = None

if "selected_modules" not in st.session_state:
    st.session_state.selected_modules = []

if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []

if "results" not in st.session_state:
    st.session_state.results = {}

if "show_details" not in st.session_state:
    st.session_state.show_details = False

# ---------- MODULES & ACTIONS ----------
MODULES = [f"Module {i}" for i in range(1, 13)]
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
st.write("")

# ---------- HOME PAGE ----------
if st.session_state.page == "home":
    st.subheader("Choose how you want to proceed")
    col1, col2 = st.columns(2)

    if col1.button("Search by KEN"):
        st.session_state.page = "ken_search"
        st.session_state.show_details = False
        st.rerun()

    if col2.button("Browse Modules"):
        st.session_state.page = "module_browser"
        st.session_state.show_details = False
        st.rerun()

# ---------- KEN SEARCH PAGE ----------
elif st.session_state.page == "ken_search":
    st.subheader("KEN Search")
    ken = st.text_input("Enter KEN Number")

    if st.button("Search"):
        if ken.strip() == "":
            st.error("Please enter a KEN number")
        else:
            st.session_state.ken_number = ken
            st.session_state.electrification = f"AC 25kV | Zone: Central | Section: {ken}"
            st.session_state.page = "module_browser"
            st.session_state.show_details = False
            st.rerun()

    if st.button("Back"):
        st.session_state.page = "home"
        st.session_state.show_details = False
        st.rerun()

# ---------- MODULE BROWSER PAGE ----------
elif st.session_state.page == "module_browser":
    st.subheader("Electrification")
    electrification = st.session_state.electrification or "N/A"
    st.info(electrification)

    # ---------- MODULE GRID ----------
    st.subheader("Modules")
    cols = st.columns(3)
    for i, module in enumerate(MODULES):
        col = cols[i % 3]
        selected = module in st.session_state.selected_modules
        if col.button(module, key=module):
            if selected:
                st.session_state.selected_modules.remove(module)
            else:
                st.session_state.selected_modules.append(module)

    if st.session_state.selected_modules:
        st.write("Selected Modules:", ", ".join(st.session_state.selected_modules))

    # ---------- REPLACEMENT ACTIONS ----------
    st.subheader("Replacement Actions")
    if st.session_state.selected_modules:
        options = [f"{a} - {m}" for m in st.session_state.selected_modules for a in REPLACEMENT_ACTIONS]
        st.session_state.selected_actions = st.multiselect("Select replacement actions", options)
    else:
        st.warning("Select at least one module first")

    if st.session_state.selected_actions:
        st.write("Selected Actions:", ", ".join(st.session_state.selected_actions))

    # ---------- ACTION BUTTONS ----------
    col1, col2 = st.columns(2)

    if col1.button("Calculate MTE"):
        if not st.session_state.selected_modules:
            st.error("Select at least one module")
        elif not st.session_state.selected_actions:
            st.error("Select at least one action")
        else:
            st.session_state.results = {
                "time": "4.5 hours",
                "manpower": "3 persons",
                "overall": "13.5 hours",
                "prep": "1 hour",
                "replace": "2.5 hours",
                "final": "1 hour"
            }
            st.session_state.show_details = False
            st.success("MTE Calculated")

    if col2.button("Back to Home"):
        # Reset selections and results
        st.session_state.selected_modules = []
        st.session_state.selected_actions = []
        st.session_state.results = {}
        st.session_state.show_details = False
        st.session_state.page = "home"
        st.rerun()

    # ---------- SHOW RESULTS ----------
    if st.session_state.results:
        st.write("---")
        st.subheader("Result")
        st.text(f"KEN Number: {st.session_state.ken_number or 'N/A'}")
        st.text(f"Electrification: {electrification}")
        st.write("Selected Actions:", ", ".join(st.session_state.selected_actions))
        st.text(f"Time: {st.session_state.results['time']}")
        st.text(f"Manpower: {st.session_state.results['manpower']}")
        st.success(f"Overall MTE: {st.session_state.results['overall']}")

        # ---------- SHOW DETAILS ----------
        if st.button("Show Details"):
            st.session_state.show_details = True

        if st.session_state.show_details:
            st.info(
                f"""
Preparation : {st.session_state.results['prep']}
Replacement : {st.session_state.results['replace']}
Finalisation : {st.session_state.results['final']}
"""
            )
