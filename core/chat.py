import streamlit as st

def chat():
    st.subheader("Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender.capitalize()}**: {msg}")
    user_input = st.text_input("Type your message")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", f"You said: {user_input}"))