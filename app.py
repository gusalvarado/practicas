import streamlit as st
from core.chat import chat
from tools.auth import Authenticator
from tools.sessions import get_session

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

    menu = ["Chat"] if user["role"] == "admin" else ["Chat"]
    st.session_state.view = st.radio("Navigate", menu, horizontal=True)

    st.write("Session ID:", st.session_state.get("session_id"))
    st.write("Authenticated:", st.session_state.get("authenticated"))
    st.write("User Info:", st.session_state.get("user_info"))

    match st.session_state.view:
        case "Chat":
            chat()
        case _:
            st.error("Invalid view")