import streamlit as st
from tools.auth import Authenticator

def signup():
    st.title("Create a new account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        name = st.text_input("Full name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submitted = st.form_submit_button("Signup up")

    if submitted:
        if not username or not name or not password or not confirm_password:
            st.warning("missing fields required")
        elif password != confirm_password:
            st.error("Passwords do not match")
        else:
            try:
                auth = Authenticator()
                auth.create_user(username, name, password, role)
                st.success("User created succesfully!")
            except Exception as e:
                st.error(f"Error creating user: {e}")