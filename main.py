import streamlit as st

st.set_page_config(page_title="GreenLens AI Home")

st.title("🌿 GreenLens AI: Urban Monitoring")
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