import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/api")
idea = st.text_input("Enter your idea:")
if st.button("Expand"):
  response = requests.post(f"{API_URL}/expand", json={"idea": idea})
  st.write(response.json()["expanded_idea"])