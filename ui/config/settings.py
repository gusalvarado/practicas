# ui/config/settings.py
"""
Configuration settings for the dashboard
"""

import streamlit as st
from ui.utils.helpers import load_favicon

def configure_page():
    """Configure the Streamlit page settings"""
    favicon = load_favicon()

    st.set_page_config(
        page_title="Content Research Dashboard",
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/issues',
            'Report a bug': 'https://github.com/your-repo/issues',
            'About': """
            # Content Research Dashboard

            This application uses CrewAI and AWS Bedrock to perform comprehensive research on any topic.

            **Features:**
            - AI-powered research team
            - Multiple report formats
            - Customizable themes
            - Report downloads
            """
        }
    )

# App metadata
APP_INFO = {
    "name": "Content Research Dashboard",
    "version": "1.0.0",
    "description": "AI-powered research dashboard using CrewAI and AWS Bedrock",
    "author": "Your Name",
    "contact": "your.email@example.com"
}

# Research settings
RESEARCH_CONFIG = {
    "default_output_dir": "output",
    "default_report_filename": "report.md",
    "max_topic_length": 200,
    "spinner_text": "🔍 Investigating... This may take a few minutes."
}
