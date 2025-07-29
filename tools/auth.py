import os
import bcrypt
import psycopg2
import functools
import streamlit as st
from psycopg2 import pool

def admin_only(func):
    """Restrict access to admin users only"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = st.session_state.get("user_info")
        if user and user.get("role") == "admin":
            return func(*args, **kwargs)
        else:
            st.warning("You don't have permission to access this page")
        return None
    return wrapper

def role_required(allowed_roles):
    """Restrict access to users with specified roles"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = st.session_state.get("user_info")
            if user and user.get("role") in allowed_roles:
                return func(*args, **kwargs)
            else:
                st.warning(f"You don't have permission to access this page")
        return wrapper
    return decorator

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

class Authenticator:
    def check_credentials(self, username: str, password: str):
        try:
            db_pool = get_connection_pool()
            conn = db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT name, password_hash, role FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            conn.close()

            if row and bcrypt.checkpw(password.encode(), row[1].encode()):
                return {"name": row[0], "role": row[2]}
            return None

        except psycopg2.InterfaceError:
            st.error("Could not connect to the database")
            return None
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None
    
    def create_user(self, username: str, name: str, password: str, role: str):
        db_pool = get_connection_pool()
        conn = db_pool.getconn()
        cursor = conn.cursor()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO users (username, name, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, name, hashed, role)
        )
        conn.commit()
        conn.close()
        db_pool.putconn(conn)

    def login(self):
        st.title("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                user_info = self.check_credentials(username, password)
                if user_info:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    st.success(f"Welcome, {user_info['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    def logout(self):
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()