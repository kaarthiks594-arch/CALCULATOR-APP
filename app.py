import streamlit as st

st.set_page_config(page_title="MTE Calculator", layout="centered")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "menu"

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

# ---------- MODULE LIST ----------
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

# ---------- MENU PAGE ----------
if st.session_state.page == "menu":
    st.subheader("Choose how you want to proceed")
    col1, col2 = st.columns(2)

    if col1.button("Search by KEN"):
        st.session_state.page = "search"
        st.rerun()

    if col2.button("Browse Modules"):
        st.session_state.page = "browse"
        st.rerun()

# ---------- PAGE 1 : KEN SEARCH ----------
elif st.session_state.page == "search":
    st.subheader("KEN Search")
    ken = st.text_input("Enter KEN Number")

    if st.button("Search"):
        if ken.strip() == "":
            st.error("Please enter a KEN number")
        else:
            st.session_state.ken_number = ken
            st.session_state.electrification = f"AC 25kV | Zone: Central | Section: {ken}"
            st.session_state.page = "details"
            st.rerun()

# ---------- PAGE 2 : BROWSE MODULES ----------
elif st.session_state.page == "browse":
    st.subheader("Browse Modules")

    cols = st.columns(3)
    for i, module in enumerate(MODULES):
        col = cols[i % 3]
        selected = module in st.session_state.selected_modules

        if col.button(module, key=module, use_container_width=True):
            if selected:
                st.session_state.selected_modules.remove(module)
            else:
                st.session_state.selected_modules.append(module)

    # Show selected modules
    if st.session_state.selected_modules:
        st.write("Selected Modules")
        cols = st.columns(len(st.session_state.selected_modules))
        for i, module in enumerate(st.session_state.selected_modules):
            with cols[i]:
                st.info(module)

    if st.button("Proceed to Replacement Actions"):
        if len(st.session_state.selected_modules) == 0:
            st.warning("Select at least one module to proceed")
        else:
            st.session_state.page = "details"
            st.rerun()
