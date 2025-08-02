import streamlit as st
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory

session_id = st.session_state.get("session_id")

history = DynamoDBChatMessageHistory(
    table_name="chat-memory",
    session_id=session_id,
)