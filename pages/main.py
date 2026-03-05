import streamlit as st

# 1. Hide the default navigation sidebar list
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- CUSTOM SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 Navigation")

# This creates a clean link to your map.py file
st.sidebar.page_link("map.py", label="Interactive Map", icon="🌐")

st.sidebar.write("---")

st.set_page_config(page_title="GreenLens")

st.title("🌿 Davao City: Urban Green Space Monitoring")
st.header("CPE126L - Group 6")

st.write("""
Welcome to our Engineering Project! Use the **Sidebar** on the left 
to navigate between our tools.
""")

st.subheader("Our Team:")
members = ["Member Name 1", "Member Name 2", "Member Name 3"]

for member in members:
    st.write(f"- {member}")

st.info("👈 Click on 'Explorer' in the sidebar to see the Davao City Map!")