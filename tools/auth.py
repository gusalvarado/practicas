import os
import uuid
import bcrypt
import functools
import streamlit as st
from psycopg2 import pool
from tools.sessions import set_session, get_session, delete_session
from streamlit_cookies_controller import CookieController

cookie = CookieController()

@st.cache_resource
def get_connection_pool():
    return pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "kurso_db"),
        user=os.getenv("DB_USER", "kurso"),
        password=os.getenv("DB_PASSWORD", "kurso34")
    )

def admin_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = st.session_state.get("user_info")
        if user and user.get("role") == "admin":
            return func(*args, **kwargs)
        st.warning("You don't have permission to access this page")
    return wrapper

def role_required(allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = st.session_state.get("user_info")
            if user and user.get("role") in allowed_roles:
                return func(*args, **kwargs)
            st.warning("You don't have permission to access this page")
        return wrapper
    return decorator

class Authenticator:
    def _get_conn(self):
        return get_connection_pool().getconn()
    
    def _return_conn(self, conn):
        get_connection_pool().putconn(conn)

    def check_credentials(self, username: str, password: str):
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT name, password_hash, role FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            conn.close()
            if row and bcrypt.checkpw(password.encode(), row[1].encode()):
                return {"name": row[0], "role": row[2]}
            return None
        except Exception as e:
            st.error(f"Database error: {e}")
            return None

    def create_user(self, username: str, name: str, password: str, role: str):
        conn = self._get_conn()
        cursor = conn.cursor()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO users (username, name, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, name, hashed, role)
        )
        conn.commit()
        conn.close()

    def login(self):
        st.title("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            user_info = self.check_credentials(username, password)
            if user_info:
                session_id = str(uuid.uuid4())
                set_session(session_id, user_info)
                cookie.set("session_id", session_id, max_age=86400)  # 1 day
                st.session_state.update({
                    "authenticated": True,
                    "user_info": user_info,
                    "session_id": session_id,
                })
                st.success(f"Welcome, {user_info['name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    def restore_session(self):
        if st.session_state.get("authenticated"):
            return  # Already authenticated

        session_id = cookie.get("session_id")
        if session_id and not st.session_state.get("user_info"):
            user_info = get_session(session_id)
            if user_info:
                st.session_state.update({
                    "authenticated": True,
                    "user_info": user_info,
                    "session_id": session_id,
                })

    def logout(self):
        if st.sidebar.button("Logout"):
            session_id = st.session_state.get("session_id")
            if session_id:
                delete_session(session_id)
                cookie.delete("session_id")
            st.session_state.clear()
            st.rerun()