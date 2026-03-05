import streamlit as st
import leafmap.foliumap as leafmap

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Davao Urban Green Space")
st.title("Davao City: Automated Urban Green Space Monitoring")

# 2. Tabs to separate Map and Analysis
tab1, tab2 = st.tabs(["🌐 Interactive Map", "📊 Comparison Analysis"])

with tab1:
    st.header("Interactive Satellite Reference")
    st.write("Explore the current urban landscape of Davao City.")

    # Render the ordinary satellite map (Requirement #1)
    # This uses the coordinates for Davao City
    m = leafmap.Map(center=[7.0707, 125.6087], zoom=14)
    m.add_basemap("HYBRID")
    m.to_streamlit(height=600)

    # Direct External Links for verification
    st.write("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("🕒 Open Google Earth Historical Imagery",
                       "https://earth.google.com/web/@7.0707,125.6087,500a,35y,0h,0t,0r")
    with col_b:
        # Link to the official zoning map
        st.link_button("🗺️ Open Official Davao Zoning Map",
                       "https://map.davaocity.gov.ph/zoning/")

with tab2:
    st.header("AI Classification Results (2020 vs 2025)")
    st.info("AI Technique: Image-Based Classification with Texture Analysis.")

    # Side-by-side comparison of local images (Requirement #2)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("September 2020 Baseline")
        # Ensure 2020.png is pushed to your GitHub
        st.image("2020.png", use_container_width=True, caption="Initial vegetation density.")

    with col2:
        st.subheader("September 2025 Current")
        # Ensure 2025.png is pushed to your GitHub
        st.image("2025.png", use_container_width=True, caption="Detected vegetation loss.")

    st.write("---")
    st.markdown("""
    **Project Logic**: 
    Our system divides Davao City into a **grid of small zones**. 
    By cross-referencing these classified patches with the official zoning map link in Tab 1, 
    we can determine if green space loss is occurring in protected **Forest** or **Water Resource** zones.
    """)