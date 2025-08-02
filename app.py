import streamlit as st
from core.chat import chat
from tools.auth import Authenticator
from core.admin import admin

auth = Authenticator()
auth.restore_session()

st.session_state.setdefault("view", "Home")

if not st.session_state.get("authenticated"):
    auth.login()
    st.stop()
else:
    auth.logout()
    user = st.session_state.user_info
    st.sidebar.success(f"{user['name']} ({user['role']})")

    menu = ["Chat", "Admin"] if user["role"] == "admin" else ["Chat"]
    st.session_state.view = st.radio("Navigate", menu, horizontal=True)

    match st.session_state.view:
        case "Chat":
            chat()
        case "Admin":
            admin()
        case _:
            st.error("Invalid view")