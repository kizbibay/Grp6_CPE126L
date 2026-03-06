import streamlit as st
import pandas as pd
import plotly.express as px
import cv2
import numpy as np
import os
from skimage.feature import graycomatrix, graycoprops


# ---------------------------------
# IMAGE PREPARATION
# ---------------------------------

def pad_to_grid(img, grid_size):
    h, w = img.shape[:2]

    pad_h = (grid_size - h % grid_size) % grid_size
    pad_w = (grid_size - w % grid_size) % grid_size

    return cv2.copyMakeBorder(
        img,
        0, pad_h,
        0, pad_w,
        cv2.BORDER_CONSTANT,
        value=[0,0,0]
    )


# ---------------------------------
# VEGETATION INDEX (Pseudo NDVI)
# ---------------------------------

def vegetation_index(img):

    img = img.astype("float")

    R = img[:,:,2]
    G = img[:,:,1]
    B = img[:,:,0]

    exg = 2*G - R - B

    return exg


# ---------------------------------
# TEXTURE FEATURES
# ---------------------------------

def extract_texture_features(patch):

    gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

    glcm = graycomatrix(
        gray,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    contrast = graycoprops(glcm, 'contrast')[0,0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0,0]

    return contrast, homogeneity


# ---------------------------------
# GRID ANALYSIS
# ---------------------------------

def process_analysis(img, grid_size):

    height, width, _ = img.shape

    overlay = img.copy()
    output = img.copy()

    veg_boxes = 0
    total_boxes = 0

    urban_mask = []

    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):

            patch = img[y:y+grid_size, x:x+grid_size]

            total_boxes += 1

            # vegetation index
            exg = vegetation_index(patch)

            veg_mask = exg > 20

            green_percent = np.sum(veg_mask) / veg_mask.size * 100

            # texture filter
            contrast, homogeneity = extract_texture_features(patch)

            if green_percent > 50 and homogeneity < 0.6:

                color = (0,255,0)
                veg_boxes += 1
                urban_mask.append(0)

            elif green_percent > 15:

                color = (0,255,255)
                veg_boxes += 1
                urban_mask.append(0)

            else:

                color = (0,0,255)
                urban_mask.append(1)

            cv2.rectangle(
                overlay,
                (x,y),
                (x+grid_size,y+grid_size),
                color,
                -1
            )

            cv2.rectangle(
                output,
                (x,y),
                (x+grid_size,y+grid_size),
                (255,255,255),
                1
            )

    cv2.addWeighted(overlay,0.40,output,0.60,0,output)

    veg_ratio = (veg_boxes / total_boxes) * 100 if total_boxes > 0 else 0

    return output, veg_ratio, np.array(urban_mask)


# ---------------------------------
# MULTI YEAR TREND
# ---------------------------------

def calculate_trend(grid_size):

    years=[]
    veg_values=[]

    for year in range(2020,2026):

        path=f"images/{year}.png"

        if os.path.exists(path):

            img=cv2.imread(path)

            img=pad_to_grid(img,grid_size)

            _,ratio,_=process_analysis(img,grid_size)

            years.append(year)
            veg_values.append(ratio)

    df=pd.DataFrame({
        "Year":years,
        "Vegetation %":veg_values
    })

    return df


# ---------------------------------
# STREAMLIT DASHBOARD
# ---------------------------------

def show_grid_analysis():

    st.title("Urban Vegetation & Urbanization Analysis")

    available_years=[str(y) for y in range(2020,2026)]

    col1,col2=st.columns(2)

    with col1:
        baseline_year=st.selectbox(
            "Baseline Year",
            available_years,
            index=2
        )

    with col2:
        current_year=st.selectbox(
            "Comparison Year",
            available_years,
            index=5
        )

    st.sidebar.title("Analysis Settings")

    grid_size=st.sidebar.slider(
        "Grid Size",
        20,
        100,
        40
    )

    if st.button("Run Analysis"):

        base_path=f"images/{baseline_year}.png"
        curr_path=f"images/{current_year}.png"

        colA,colB=st.columns(2)

        results={}

        # BASELINE
        if os.path.exists(base_path):

            img=cv2.imread(base_path)

            img=pad_to_grid(img,grid_size)

            proc,ratio,urban_base=process_analysis(img,grid_size)

            results["base"]=ratio

            with colA:

                st.subheader(f"{baseline_year}")

                st.image(proc,channels="BGR")

                st.write(f"Vegetation: {ratio:.2f}%")

        # CURRENT
        if os.path.exists(curr_path):

            img=cv2.imread(curr_path)

            img=pad_to_grid(img,grid_size)

            proc,ratio,urban_curr=process_analysis(img,grid_size)

            results["curr"]=ratio

            with colB:

                st.subheader(f"{current_year}")

                st.image(proc,channels="BGR")

                st.write(f"Vegetation: {ratio:.2f}%")

        # LEGEND

        st.markdown("""

        **Grid Patch Key**

        🟩 High Vegetation (>50%)  
        🟨 Moderate Vegetation (15-50%)  
        🟥 Urban / Low Vegetation (<15%)

        """)

        # TREND REPORT

        if "base" in results and "curr" in results:

            st.header("Urbanization Trend Report")

            veg_base=results["base"]
            veg_curr=results["curr"]

            data={

                "Category":["Vegetated","Urban"],

                f"{baseline_year}":[veg_base,100-veg_base],

                f"{current_year}":[veg_curr,100-veg_curr]

            }

            df=pd.DataFrame(data)

            colC,colD=st.columns([1,1.5])

            with colC:

                st.table(df)

                change=veg_curr-veg_base

                if change>0:
                    st.success(
                        f"Vegetation increased by {change:.2f}%"
                    )
                else:
                    st.warning(
                        f"Vegetation declined by {abs(change):.2f}%"
                    )

            with colD:

                melt=pd.melt(
                    df,
                    id_vars=["Category"],
                    var_name="Year",
                    value_name="Percent"
                )

                fig=px.bar(
                    melt,
                    x="Year",
                    y="Percent",
                    color="Category",
                    barmode="group",
                    template="plotly_dark"
                )

                st.plotly_chart(fig,use_container_width=True)

        # MULTI YEAR TREND

        st.header("Vegetation Trend (2020-2025)")

        trend_df=calculate_trend(grid_size)

        if len(trend_df)>0:

            fig=px.line(
                trend_df,
                x="Year",
                y="Vegetation %",
                markers=True,
                template="plotly_dark"
            )

            st.plotly_chart(fig,use_container_width=True)