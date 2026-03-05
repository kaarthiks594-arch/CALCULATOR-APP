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
    st.session_state.show_details = {}

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
        st.session_state.show_details = {}
        st.rerun()
    if col2.button("Browse Modules"):
        st.session_state.page = "module_browser"
        st.session_state.show_details = {}
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
            st.session_state.show_details = {}
            st.rerun()
    if st.button("Back"):
        st.session_state.page = "home"
        st.session_state.show_details = {}
        st.rerun()

# ---------- MODULE BROWSER PAGE ----------
elif st.session_state.page == "module_browser":

    # ---------- CONDITIONAL ELECTRIFICATION ----------
    if st.session_state.ken_number.strip():
        st.subheader("Electrification")
        st.info(st.session_state.electrification)

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

    # ---------- ACTION BUTTONS ----------
    col1, col2 = st.columns(2)
    if col1.button("Calculate MTE"):
        if not st.session_state.selected_modules:
            st.error("Select at least one module")
        elif not st.session_state.selected_actions:
            st.error("Select at least one action")
        else:
            # Generate results per action
            st.session_state.results = {}
            for action in st.session_state.selected_actions:
                st.session_state.results[action] = {
                    "time": "4.5",
                    "manpower": "3",
                    "prep": "1",
                    "replace": "2.5",
                    "final": "1"
                }
            st.success("MTE Calculated")

    if col2.button("Back to Home"):
        st.session_state.selected_modules = []
        st.session_state.selected_actions = []
        st.session_state.results = {}
        st.session_state.show_details = {}
        st.session_state.page = "home"
        st.rerun()

    # ---------- SHOW RESULTS IN VERTICAL ----------
    if st.session_state.results:
        st.write("---")
        st.subheader("Result")
        for action_name, values in st.session_state.results.items():
            st.write(f"**{action_name}**")
            cols = st.columns([2, 2, 1])
            cols[0].write("Time")
            cols[0].text(values["time"])
            # Button for popup
            if cols[1].button("Time Split", key=f"time_split_{action_name}"):
                st.session_state.show_details[action_name] = True
            cols[2].write("Manpower")
            cols[2].text(values["manpower"])

            # ---------- POPUP ----------
            if st.session_state.show_details.get(action_name):
                st.info(
                    f"""
1. Preparation : {values['prep']}
2. Replacement : {values['replace']}
3. Finalisation : {values['final']}
"""
                )
