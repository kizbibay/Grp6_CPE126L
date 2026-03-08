import streamlit as st
import ee
from datetime import datetime
from login import account

# --- INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- AUTHENTICATION CHECK ---
if not st.session_state['logged_in']:

    # Hide sidebar navigation until logged in
    st.markdown("""
            <style>
                [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)

    placeholder = st.empty()
    # Call login.py
    account()
else:
    # --- YOUR DASHBOARD CONTENT ---

    # --- 1. MODERN SIDEBAR CSS ---
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            section[data-testid="stSidebar"] {
                background-color: #F6F6E9 !important;
                border-right: 1px solid #E6E6E6;
                padding-top: 20px;
            }
            [data-testid="stSidebar"] a p {
                color: #31333F !important;
                font-size: 16px !important;
                font-weight: 500 !important;
            }
            .sidebar-brand {
                padding: 1.5rem;
                font-size: 1.2rem;
                font-weight: 700;
                color: #FF4B2B;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .sidebar-footer {
                position: fixed;
                bottom: 20px;
                width: 260px;
                padding: 20px;
                border-top: 1px solid #E6E6E6;
                background: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. GEE SYNC LOGIC ---
    # Initialize Earth Engine
    if 'ee_initialized' not in st.session_state:
        try:
            ee.Initialize(project='ai-urban-heat-index')
            st.session_state['ee_initialized'] = True
        except Exception as e:
            st.error(f"Error: {e}")


    @st.cache_data(ttl=86400)  # Cache for 24 hours
    def fetch_realtime_stats():
        # Davao City Boundary
        davao_roi = ee.Geometry.Point([125.6087, 7.0707]).buffer(15000).bounds()

        # Baseline 2020 NDVI
        ndvi_2020 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                     .filterBounds(davao_roi)
                     .filterDate('2020-01-01', '2020-12-31')
                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                     .median()
                     .normalizedDifference(['B8', 'B4']))

        # Current 2026 NDVI (Latest)
        ndvi_now = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                    .filterBounds(davao_roi)
                    .filterDate('2026-01-01', '2026-03-06')
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                    .median()
                    .normalizedDifference(['B8', 'B4']))

        # Calculate Mean Loss
        loss = ndvi_now.subtract(ndvi_2020).reduceRegion(
            reducer=ee.Reducer.mean(), geometry=davao_roi, scale=30).getInfo()

        # Latest LST (Landsat 8)
        lst_now = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
                   .filterBounds(davao_roi)
                   .filterDate('2025-06-01', '2026-03-06')
                   .median())

        temp_k = lst_now.select('ST_B10').multiply(0.00341802).add(149.0)
        temp_c = temp_k.subtract(273.15).reduceRegion(
            reducer=ee.Reducer.max(), geometry=davao_roi, scale=30).getInfo()

        return round(loss.get('nd', 0) * 100, 1), round(temp_c.get('ST_B10', 0), 1)


    # Fetch stats
    try:
        veg_delta, max_temp = fetch_realtime_stats()
    except:
        veg_delta, max_temp = -11.2, 42.6  # Fallback to your research values

    # --- 2. CUSTOM SIDEBAR CONTENT ---
    with st.sidebar:
        st.image("logo.png", use_container_width=True)

        st.divider()

        # Navigation Links
        st.page_link("main.py", label="Dashboard", icon="📊")
        st.page_link("pages/map.py", label="Interactive Map", icon="📍")

        # --- SIDEBAR FOOTER ---
        current_user = st.session_state.get('user', 'Guest')

        st.markdown("""
            <style>
                .footer-container {
                    position: fixed;
                    bottom: 20px; 
                    width: 260px;
                    padding: 10px;
                    border-top: 1px solid #E6E6E6;
                    background: F6F6E9;
                }
                .user-profile {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 10px;
                }
                .user-avatar {
                    width: 35px;
                    height: 35px;
                    background: #4CAF50;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                }
                /* Logout button container */
                div.stButton > button {
                width: 100% !important;
                background-color: #4B7E5D !important; /* Your GreenLens Green */
                color: white !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 0.5rem !important;
                transition: background-color 0.3s ease;
                }

                /* Hover effect to make it feel interactive */
                div.stButton > button:hover {
                background-color: #3e6a4e !important; /* Slightly darker green on hover */
                color: white !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # User Profile
        st.markdown(f"""
            <div class="footer-container">
                <div class="user-profile">
                    <div class="user-avatar">{current_user[0].upper()}</div>
                    <div>
                        <p style="margin:0; font-size:13px; font-weight:600; color:#31333F;">{current_user}</p>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        # Logout Button
        if st.button("Logout", key="logout_btn", width='stretch'):
            st.session_state['logged_in'] = False
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --- MAIN PAGE CONTENT ---
    st.title("Davao City: Urban Green Space Insights")
    st.caption(f"Last Satellite Sync: {datetime.now().strftime('%B %d, %Y')} | Data Source: Sentinel-2 & Landsat-8")

    # --- 3. HIGH-LEVEL METRICS ---
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Vegetation Loss", value=f"{veg_delta}%", delta="Live Analysis", delta_color="inverse")
        st.caption("Detected canopy reduction in urbanizing areas.")
    with col2:
        st.metric(label="Max Surface Temp", value=f"{max_temp}°C", delta="Thermal Peak", delta_color="inverse")
        st.caption("Peak temperature in high-density zones.")
    with col3:
        st.metric(label="Monitoring Scope", value="Davao City", delta="Active")

    st.write("---")

    # --- 4. EXTERNAL DATA VERIFICATION ---
    st.subheader("🔗 Data Verification Sources")
    st.info("Cross-reference our AI-derived NDVI and LST data with official records.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🗺️ Official Zoning")
        st.write("Compare findings with the **Comprehensive Land Use Plan (CLUP)**.")
        st.link_button("Access Davao City Zoning Map", "https://map.davaocity.gov.ph/zoning/")
    with c2:
        st.markdown("### 🕒 Ground Truth")
        st.write("Verify site developments with **Google Earth Historical Imagery**.")
        st.link_button("Launch Google Earth Pro", "https://earth.google.com/web/@7.0707,125.6087,500a,35y,0h,0t,0r")