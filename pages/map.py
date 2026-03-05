import streamlit as st
import leafmap.foliumap as leafmap

# 1. Page Configuration
st.set_page_config(layout="wide")
st.title("Davao City: Urban Green Space Monitoring (2020-2025)")

# 2. Context from your Project Slides
st.info("AI Technique: Computer Vision using Texture Analysis for Grid-Zone Classification.")

# 3. Interactive Map (Requirement #1)
# This serves as the 'Ordinary Satellite Map' for current visualization
st.subheader("Interactive Study Area Map")
m = leafmap.Map(center=[7.0707, 125.6087], zoom=14)
m.add_basemap("HYBRID") # Provides labels for Davao City landmarks
m.to_streamlit(height=600)

# 4. External Analysis Link (Requirement #2)
# This replaces the broken time-slider with a functional link to historical data
st.write("---")
st.header("Comparison Analysis: 2020 vs 2025")
st.markdown("""
Our system independently classifies each patch of the map as **"Vegetated"** or **"Urban"**. 
To verify these changes using high-resolution **Historical Imagery**, please use the Google Earth link below:
""")

# High-precision link to Davao City study area
google_earth_url = "https://earth.google.com/web/@7.0707,125.6087,500a,35y,0h,0t,0r"

st.link_button("🌐 Open Historical Imagery in Google Earth", google_earth_url)

# 5. Summary Metrics
st.write("---")
col1, col2, col3 = st.columns(3)
col1.metric("Analysis Period", "2020 - 2025")
col2.metric("Primary Region", "Davao City")
col3.metric("Data Source", "Google Earth Pro")