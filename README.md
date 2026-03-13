# 🌿 GreenLens: Automated Urban Green Space Monitoring

**GreenLens** is an automated environmental monitoring system designed to quantify and visualize vegetation loss in **Davao City** using satellite imagery and computer vision. This project was developed as part of the **CPE126L** course by Group 6.

## 🚀 Project Overview
As urban areas expand, monitoring the vegetation and urban coverage is critical for urban planning and mitigating the **Urban Heat Island** effect. GreenLens provides a dual-layer approach:
1.  **Core Analysis**: An OpenCV-driven grid classification system that identifies land-use changes at the patch level.
2.  **Visualization**: An interactive map powered by Google Earth Engine for real-time NDVI and LST roaming.

## 🛠️ Features
* **Grid Classification (analysis.py)**: Uses HSV color-space thresholding to classify land into "Vegetated," "Urban," or "Transitional Soil".
* **Interactive Mapping (map.py)**: Real-time toggling of **NDVI** (Vegetation Index) and **LST** (Surface Temperature) layers.
* **Trend Report**: Automated generation of land-cover statistics and bar charts comparing baseline vs. current data.

## 📂 Repository Structure
* `main.py`: The primary dashboard entry point and project summary.
* `pages/`: Contains the modular application files for the map and analysis tools.
* `images/`: Local satellite assets used for the Grid Classification engine.
* `requirements.txt`: Python dependencies required to run the project.

## ⚙️ Installation & Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/kizbibay/Grp6_CPE126L.git](https://github.com/kizbibay/Grp6_CPE126L.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Authentication:**
    Ensure you have a Google Earth Engine account. The app will prompt you for authentication on the first run.
4.  **Run the App:**
    ```bash
    streamlit run main.py
    ```

## 🛠️ Troubleshooting & Authentication

#### **Google Earth Engine (GEE) Authentication**
The **Interactive Map** tab requires a valid GEE account. 
* **First-Run Auth**: Check your terminal for a link. Open it, sign in, and paste the verification code back into the terminal to generate your local credentials.

#### **Missing Grid Patches**
* **Image Path**: Verify that the `images/` folder is in the root directory and contains `.png` files named exactly by year (e.g., `2020.png`).

## 👥 Project Team (Group 6)
* **Kiziahlyn Fiona Bibay**
* **Bea Mae D. Valeriano**
* **Shetty Alaisa H. Jajalis**
