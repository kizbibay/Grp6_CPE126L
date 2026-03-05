import streamlit as st
import ee
import leafmap.foliumap as leafmap

# 1. Initialize Earth Engine
try:
    ee.Initialize(project='ai-urban-heat-index')
except Exception as e:
    st.error(f"Authentication Error: {e}")

st.set_page_config(layout="wide")
st.title("Davao City: Urban Green Space Monitoring (2020-2025)")

tab1, tab2 = st.tabs(["🌐 Interactive Map", "📊 Comparison Analysis"])

with tab1:
    # --- TOP-POSITIONED VERIFICATION LINKS ---
    col_link1, col_link2 = st.columns(2)
    with col_link1:
        st.link_button("🕒 Google Earth Historical Imagery",
                       "https://earth.google.com/web/@7.0707,125.6087,500a,35y,0h,0t,0r")
    with col_link2:
        st.link_button("🗺️ Official Davao Zoning Map",
                       "https://map.davaocity.gov.ph/zoning/")

    st.write("---")

    # --- NDVI RANGE CALCULATION ---
    lat, lon = [7.0707, 125.6087]
    roi = ee.Geometry.Point(lon, lat).buffer(5000).bounds()


    def get_ndvi(year):
        img = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
               .filterBounds(roi)
               .filterDate(f'{year}-01-01', f'{year}-12-31')
               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
               .median()
               .clip(roi))
        return img.normalizedDifference(['B8', 'B4']).rename(f'NDVI_{year}')


    ndvi_2020 = get_ndvi(2020)
    ndvi_2025 = get_ndvi(2025)

    # Calculate Difference: (2025 - 2020)
    # Negative values (Red) = Vegetation Loss
    # Positive values (Green) = Vegetation Gain
    ndvi_change = ndvi_2025.subtract(ndvi_2020).rename('NDVI_Change')

    # --- MAP RENDERING ---
    m = leafmap.Map(center=[lat, lon], zoom=14)
    m.add_basemap("HYBRID")

    # Legend Definition matching the AI Technique's classifications
    legend_dict = {
        'Vegetation Loss (Urbanization)': '#FF0000',  # Red
        'Stable / No Change': '#FFFFFF',  # White
        'Vegetation Gain (Greening)': '#008000'  # Green
    }

    # Visual parameters for the change detection map
    change_vis = {"min": -0.5, "max": 0.5, "palette": ['red', 'white', 'green']}

    m.add_ee_layer(ndvi_change, change_vis, name="NDVI Change (2020-2025)")
    m.add_legend(title="NDVI Change Key", legend_dict=legend_dict)

    m.to_streamlit(height=600)

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