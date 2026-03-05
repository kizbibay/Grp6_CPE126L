import streamlit as st
import leafmap.foliumap as leafmap

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Davao Urban Green Space")
st.title("Davao City: Automated Urban Green Space Monitoring")

# 2. Tabs to separate Map and Analysis
tab1, tab2 = st.tabs(["🌐 Interactive Map", "📊 Comparison Analysis & Zoning"])

with tab1:
    st.header("Interactive Satellite Reference")
    st.write("Explore the current urban landscape of Davao City.")

    # Render the ordinary satellite map (Requirement #1)
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
        st.link_button("🗺️ Open Official Davao Zoning Map",
                       "https://map.davaocity.gov.ph/zoning/")

with tab2:
    st.header("AI Classification & Zoning Results")
    st.info("AI Technique: Image-Based Classification with Texture Analysis.")

    # Side-by-side comparison of local images (Requirement #2)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("2020 vs 2025 Satellite Change")
        # Ensure these files are in your GitHub repository
        st.image(["2020.png", "2025.png"], width=350, caption=["Baseline (2020)", "Current (2025)"])

    with col2:
        st.subheader("Official Zoning Reference")
        # Use a screenshot of the zoning map legend since embedding is blocked
        st.image("zoning_reference.png", use_container_width=True)
        st.caption("Reference from City Planning and Development Office")

    st.write("---")
    st.markdown("""
    **Project Logic**: 
    Our system divides Davao City into a **grid of small zones**. 
    By cross-referencing our classified patches with the official zoning map, we can 
    identify if vegetation loss is occurring in protected **Forest** or **Water Resource** zones.
    """)