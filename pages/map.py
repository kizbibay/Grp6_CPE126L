import streamlit as st
import ee
import leafmap.foliumap as leafmap
from folium.plugins import MousePosition
from branca.element import MacroElement
from jinja2 import Template


st.set_page_config(layout="wide")

try:
    from pages.analysis import show_grid_analysis
except ImportError:
    from analysis import show_grid_analysis

# Hide the default navigation sidebar list
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# CUSTOM SIDEBAR
st.sidebar.title("🚀 Navigation")

# This creates a clean link to your main.py file
st.sidebar.page_link("main.py", label="Home", icon="🏠")
st.sidebar.write("---")

st.sidebar.header("Data Layers")
# Moving checkboxes to sidebar as requested
show_ndvi = st.sidebar.checkbox("Show NDVI Change (2020-2025)", value=True)
show_lst = st.sidebar.checkbox("Show LST (2025)", value=False)


# Initialize Earth Engine
if 'ee_initialized' not in st.session_state:
    try:
        ee.Initialize(project='ai-urban-heat-index')
        st.session_state['ee_initialized'] = True
    except Exception as e:
        st.error(f"Earth Engine Auth Error: {e}")

st.title("Davao City: Urban Green Space Monitoring")

tab1, tab2 = st.tabs(["🌐 Interactive Map", "📊 Comparison Analysis"])

# --- CUSTOM CLASS: DYNAMIC LEGEND ---
# This class makes the legend a "child" of the layer toggle
class BindLegend(MacroElement):
    def __init__(self, layer_name):
        super(BindLegend, self).__init__()
        self._template = Template(f"""
            {{% macro script(this, kwargs) %}}
            var legend = document.querySelector('.leaflet-control-legend');
            if (legend) {{
                this._parent.on('layeradd', function(e) {{
                    if (e.name === '{layer_name}') legend.style.display = 'block';
                }});
                this._parent.on('layerremove', function(e) {{
                    if (e.name === '{layer_name}') legend.style.display = 'none';
                }});
            }}
            {{% endmacro %}}
        """)

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


    # --- NDVI ---
    def get_ndvi_roaming(year):
        collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                      .filterDate(f'{year}-01-01', f'{year}-12-31')
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                      .median())
        return collection.normalizedDifference(['B8', 'B4']).rename(f'NDVI_{year}')

    # --- Land Surface Temperature ---
    def get_lst_roaming(year):
        """Calculates Land Surface Temperature (Celsius) using Landsat-8."""
        # Landsat 8 Collection 2 Level 2 Surface Temperature
        collection = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
                      .filterDate(f'{year}-01-01', f'{year}-12-31')
                      .filter(ee.Filter.lt('CLOUD_COVER', 20))
                      .median())

        # Thermal Band B10 scaling to Celsius
        temp_kelvin = collection.select('ST_B10').multiply(0.00341802).add(149.0)
        temp_celsius = temp_kelvin.subtract(273.15).rename(f'LST_{year}')
        return temp_celsius

    # Setup Map
    m = leafmap.Map(center=[7.0707, 125.6087], zoom=14)
    m.add_basemap("HYBRID")

    # This displays live Lat/Lon in the top-right as you move your mouse
    formatter = "function(num) {return L.Util.formatNum(num, 5) + ' º ';};"
    MousePosition(
        position='topright',
        separator=' | ',
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)

    # Define Legend
    # NDVI Visuals
    legend_dict = {
        'Vegetation Loss (Urbanization)': '#FF0000',
        'Stable / No Change': '#FFFFFF',
        'Vegetation Gain (Greening)': '#008000'
    }
    ndvi_vis = {"min": -0.5, "max": 0.5, "palette": ['red', 'white', 'green']}

    # LST Visuals: Blue (Cool) to Red (Hot)
    lst_vis = {"min": 25, "max": 45, "palette": ['blue', 'yellow', 'red']}


    # Load the Layers
    try:
        if show_ndvi:
            ndvi_2020 = get_ndvi_roaming(2020)
            ndvi_2025 = get_ndvi_roaming(2025)
            ndvi_change = ndvi_2025.subtract(ndvi_2020)

            # Name must match exactly for the legend toggle to work
            layer_name = "NDVI Change (2020-2025)"
            m.add_ee_layer(ndvi_change, ndvi_vis, name=layer_name)
            m.add_legend(title="NDVI Change Key", legend_dict=legend_dict)

            # Add the binding logic
            m.add_child(BindLegend(layer_name))

        if show_lst:
            lst_2025 = get_lst_roaming(2025)

            # Name must match exactly for the legend toggle to work
            layer_name = "LST (2025)"
            m.add_ee_layer(lst_2025, lst_vis, name=layer_name)
            m.add_legend(title="LST Key", legend_dict={"Low": "blue", "High": "red"})

            # Add the binding logic
            m.add_child(BindLegend(layer_name))
    except Exception as e:
        st.warning(f"Map data is loading: {e}")

    m.to_streamlit(height=700)


# --- TAB 2: Comparison Analysis ---
with tab2:
    show_grid_analysis()