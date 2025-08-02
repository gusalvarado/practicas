import streamlit as st
from agents.diagnostic_agent import run_diagnosis

def chat():
    st.subheader("EKS diagnostic chat")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender.capitalize()}**: {msg}")

    user_input = st.text_input("Type your message")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.spinner("Diagnosing..."):
            try:
                response = run_diagnosis(user_input)
            except Exception as e:
                response = f"Error: {str(e)}"
        st.session_state.chat_history.append(("bot", response))
        st.rerun()