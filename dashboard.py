import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://backend:8080")
idea = st.text_input("Enter your idea:")
if st.button("Expand"):
  response = requests.post(f"{API_URL}/expand", json={"idea": idea})
  try:
    data = response.json()
    st.write(data["expanded_idea"])
  except requests.exceptions.JSONDecodeError:
    st.error("Invalid response from server")
  except Exception as e:
    st.error(f"Error: {e}")