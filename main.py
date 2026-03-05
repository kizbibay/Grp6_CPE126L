import streamlit as st

# --- 1. MODERN SIDEBAR CSS ---
st.markdown("""
    <style>
        /* Hide default navigation list */
        [data-testid="stSidebarNav"] {display: none;}
        
        /* Modern Sidebar Container Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E6E6E6;
            padding-top: 20px;
        }
        
        /* Targets the text inside all sidebar page links */
        [data-testid="stSidebar"] a p {
            color: #31333F !important;
            font-size: 16px !important;
            font-weight: 500 !important;
        }
        
        /* Sidebar Heading/Title Styling */
        .sidebar-brand {
            padding: 1.5rem;
            font-size: 1.2rem;
            font-weight: 700;
            color: #FF4B2B; /* Brand Color */
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Profile/Footer Section at bottom of sidebar */
        .sidebar-footer {
            position: fixed;
            bottom: 20px;
            width: 260px;
            padding: 10px;
            border-top: 1px solid #E6E6E6;
            background: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. CUSTOM SIDEBAR CONTENT ---
with st.sidebar:
    # --- BRANDING ---
    st.markdown(
        '<div class="sidebar-brand">🌿 GreenLens <span style="font-size:10px; background:#F0F2F6; padding:2px 6px; border-radius:4px; color:#666;">PRO</span></div>',
        unsafe_allow_html=True)

    st.write("")  # Spacer

    # --- NAVIGATION ITEMS ---
    # Using icons and labels
    st.page_link("main.py", label="Dashboard", icon="📊")
    st.page_link("pages/map.py", label="Location Overview", icon="📍")
    st.write("---")

    # --- TEAM / SETTINGS SECTION ---
    st.page_link("main.py", label="Support", icon="❓")
    st.page_link("main.py", label="Settings", icon="⚙️")

    # --- SIDEBAR FOOTER (Profile Section) ---
    st.markdown("""
        <div class="sidebar-footer">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 35px; height: 35px; background: #4CAF50; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                    K
                </div>
                <div>
                    <p style="margin:0; font-size:13px; font-weight:600; color:#31333F;">Kiziahlyn Fiona</p>
                    <p style="margin:0; font-size:11px; color:#666;">Group 6 Lead</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN PAGE CONTENT ---
st.title("Welcome to your Monitoring Dashboard")