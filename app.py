import streamlit as st
from core.chat import chat
from tools.auth import Authenticator
# from core.admin import admin
# from core.signup import signup

auth = Authenticator()
auth.restore_session()

st.session_state.setdefault("view", "Home")

# if not st.session_state.get("authenticated"):
#     page = st.radio("Choose page", ["Login", "Signup"], horizontal=True)
#     if page == "Login":
#         auth.login()
#     elif page == "Signup":
#         signup()
#     st.stop()
# auth.logout()
# user = st.session_state.user_info
# st.sidebar.success(f"{user['name']} ({user['role']})")

menu = ["Chat"]
st.session_state.view = st.radio("Navigate", menu, horizontal=True)

match st.session_state.view:
    case "Chat":
        chat()
    case _:
        st.error("invalid view")