import streamlit as st

def theme():
  st.set_page_config(
    page_title="Kurso AI",
    page_icon="/assets/favicon.png",
    layout="wide",
  )
  st.markdown(
    """
    <style>
    body {
      background-color: #1e1f2f;
      color: #e0e0ff;
    }
    .stApp {
      background-color: #1e1f2f;
    }
    .stButton>button {
      background-color: #5c6bc0;
      color: white;
      border-radius: 8px;
      padding: 0.5em 1em;
    }
    .stButton>button:hover {
      background-color: #7e57c2;
    }
    .stTextInput>div>input {
      background-color: #30304f;
      color: white;
    }
    .stTextInput>div>input::placeholder {
      color: #b0b0d0;
    }
    </style>
    """,
    unsafe_allow_html=True,
  )