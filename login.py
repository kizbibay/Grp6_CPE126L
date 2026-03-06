import json
import os
import hashlib
import streamlit as st

USER_DB = "users.json"


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

    with col2:
        st.markdown("""
            <div style="text-align: center; padding-bottom: 20px;">
                <h2 style="color: #4CAF50;">🌿 GreenLens PRO</h2>
                <p style="color: #666;">Secure Environmental Monitoring Access</p>
            </div>
        """, unsafe_allow_html=True)

        choice = st.tabs(["Sign In", "Create Account"])

        with choice[0]:
            user = st.text_input("Username", placeholder="Enter your username", key="l_user")
            passwd = st.text_input("Password", type="password", placeholder="Enter your password", key="l_pass")
            if st.button("Login", use_container_width=True, type="primary"):
                if verify_user(user, passwd):
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = user
                    st.rerun()
                else:
                    st.error("Invalid Username/Password")

        with choice[1]:
            new_user = st.text_input("New Username", placeholder="Choose a username", key="s_user")
            new_passwd = st.text_input("New Password", type="password", placeholder="Choose a password", key="s_pass")
            if st.button("Register", use_container_width=True):
                if save_user(new_user, new_passwd):
                    st.success("Account created! You can now Sign In.")
                else:
                    st.error("Username already exists.")