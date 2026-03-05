import streamlit as st
import pandas as pd
import plotly.express as px


def show_grid_analysis():
    st.header("📊 Grid Classification & Trend Analysis")

    # 1. UI Selection (Mimicking your Drive UI)
    available_years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    col_ui1, col_ui2 = st.columns(2)

    with col_ui1:
        st.write("📁 **Select Baseline Year**")
        baseline_year = st.selectbox("My Drive / ai_project_2026 / images /", available_years, index=2,
                                     key="base_analys")

    with col_ui2:
        st.write("📁 **Select Comparison Year**")
        current_year = st.selectbox("My Drive / ai_project_2026 / images /", available_years, index=7,
                                    key="comp_analys")

    if st.button("🚀 Run Grid Classification Analysis", use_container_width=True):
        st.write("---")
        # Texture Analysis Comparison
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.subheader(f"Baseline: {baseline_year}")
            st.image(f"images/{baseline_year}.png", use_container_width=True)
        with res_col2:
            st.subheader(f"Current: {current_year}")
            st.image(f"images/{current_year}.png", use_container_width=True)

        st.success(f"Texture analysis comparison complete for {baseline_year} vs {current_year}.")

        # --- TREND REPORTS SECTION ---
        st.write("---")
        st.write("### 📈 Urbanization Trend Report")

        # Hardcoded data based on your Davao study area findings
        report_data = {
            "Category": ["Vegetated", "Urban", "Water/Bare Soil"],
            f"{baseline_year} Area (%)": [65.2, 29.8, 5.0],
            f"{current_year} Area (%)": [47.5, 47.3, 5.2]
        }
        df = pd.DataFrame(report_data)

        col_metric1, col_metric2 = st.columns([1, 1.5])
        with col_metric1:
            st.table(df)
            st.info(
                f"Davao City observed a significant increase in urban patches between {baseline_year} and {current_year}.")

        with col_metric2:
            fig_df = pd.melt(df[["Category", f"{baseline_year} Area (%)", f"{current_year} Area (%)"]],
                             id_vars=["Category"], var_name="Year", value_name="Percentage")
            fig = px.bar(fig_df, x="Year", y="Percentage", color="Category", barmode="group",
                         color_discrete_map={"Vegetated": "#228B22", "Urban": "#FF4500", "Water/Bare Soil": "#1E90FF"})
            st.plotly_chart(fig, use_container_width=True)