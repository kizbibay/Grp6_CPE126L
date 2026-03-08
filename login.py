import json
import os
import hashlib
import streamlit as st

USER_DB = "users.json"

st.set_page_config(layout="centered")


def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)


def save_user(username, password):
    users = load_users()
    if username in users: return False
    users[username] = hash_password(password)
    with open(USER_DB, "w") as f:
        json.dump(users, f)
    return True


def verify_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False


def login_signup_ui():
    # Creating a centered layout
    _, col2, _ = st.columns([1, 2, 1])

    # --- CONTAINER COLOR ---
    st.markdown("""
        <style>
            /* 1. Targets the specific container box */
            .st-key-color_container {
                background-color: #457D58 !important;
                border: none !important;
                border-radius: 20px !important;
                padding: 30px !important;
            }

            /* 2. Fixes for text visibility inside the green box */
            [data-testid="stVerticalBlockBorderWrapper"] h2, 
            [data-testid="stVerticalBlockBorderWrapper"] p {
                color: white !important;
            }

            /* 3. Style the input labels (Username/Password) to be white */
            div[data-testid="stWidgetLabel"] p {
                color: white !important;
                font-weight: 600;
            }

            /* 4. Make the tabs text readable */
            button[data-baseweb="tab"] p {
                color: white !important;
            
            }
        
            div.stButton > button {
                background-color: #F6F6E9 !important;
                color: #4B7E5D !important;
                border: none !important;
                font-weight: bold !important;
                border-radius: 10px !important;
            }

            /* Hover effect for the button */
            div.stButton > button:hover {
                background-color: #E6E6D9 !important; /* Slightly darker cream on hover */
                color: #3e6a4e !important;
            }
            }
        </style>
    """, unsafe_allow_html=True)

    with col2:
        st.image("logo.png", width="stretch")

        with st.container(key="color_container"):
            # Header Section
            st.markdown("""
                <div style="text-align: center;">
                    <h2 style="margin-bottom: 0;">🌿 Hello!</h2>
                    <p style="font-size: 16px; opacity: 0.9; margin-top: 5px;">Welcome to GreenLens!</p>
                </div>
            """, unsafe_allow_html=True)

            choice = st.tabs(["Sign In", "Create Account"])

            with choice[0]:
                user = st.text_input("Username", placeholder="Enter your username", key="l_user")
                passwd = st.text_input("Password", type="password", placeholder="Enter your password", key="l_pass")

                if st.button("Login", width="stretch", type="primary"):
                    if verify_user(user, passwd):
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = user
                        st.rerun()
                    else:
                        st.error("Invalid Username/Password")

            with choice[1]:
                new_user = st.text_input("New Username", placeholder="Choose a username", key="s_user")
                new_passwd = st.text_input("New Password", type="password", placeholder="Choose a password",
                                           key="s_pass")
                if st.button("Register", width="stretch"):
                    if save_user(new_user, new_passwd):
                        st.success("Account created!")