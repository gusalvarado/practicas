import streamlit as st
from tools.auth import Authenticator, admin_only, role_required

auth = Authenticator()
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("user_info", None)

if not st.session_state.authenticated:
    auth.login()
else:
    auth.logout()
    user = st.session_state.user_info
    st.sidebar.success(f"Logged in as {user['name']} ({user['role']})")

@admin_only
def show_admin_page():
    st.subheader("Admin Page")
    st.write("This is the admin page")

@role_required(["admin", "user"])
def show_user_page():
    st.subheader("User Page")
    st.write("This is the user page")