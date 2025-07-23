import os
import sys
import streamlit as st
import requests
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.state_store import StateStore

st.set_page_config(page_title="IA Patito", page_icon="assets/favicon.png")
st.title("IA Patito")

# Setup session and state
session_id = st.session_state.get("session_id") or os.urandom(8).hex()
st.session_state.session_id = session_id
store = StateStore()
messages = store.load_messages(session_id)

# Chat UI layout
for msg in messages:
    with st.chat_message(msg["role"]):
        timestamp = msg.get("timestamp", "")
        st.markdown(f"{msg['content']}\n\n---\n_{timestamp}_")

# User input
prompt = st.chat_input("Pitch me an idea or ask a follow-up...")
if prompt:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Append user message
    st.chat_message("user").markdown(f"{prompt}\n\n---\n_{timestamp}_")
    messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    store.save_messages(session_id, messages)

    # Send to backend
    try:
        response = requests.post(
            os.getenv("API_URL", "http://backend:8080") + "/chat",
            json={"message": prompt, "session_id": session_id}
        )
        result = response.json()
        assistant_msg = result.get("response", "(No response from agent)")
    except Exception as e:
        assistant_msg = f"Error: {str(e)}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.chat_message("assistant").markdown(f"{assistant_msg}\n\n---\n_{timestamp}_")
    messages.append({"role": "assistant", "content": assistant_msg, "timestamp": timestamp})
    store.save_messages(session_id, messages)