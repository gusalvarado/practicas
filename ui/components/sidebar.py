# ui/components/sidebar.py
"""
Sidebar component for the dashboard
"""

import streamlit as st
from ui.styles.themes import apply_sidebar_styling, THEME_OPTIONS

def render_sidebar():
    """Render the sidebar with theme selector and information"""
    with st.sidebar:
        # Theme selector
        st.header("Theme")

        selected_theme = st.selectbox(
            "Choose sidebar color theme:",
            options=list(THEME_OPTIONS.keys()),
            index=0,
            key="theme_selector"
        )

        # Apply the selected theme
        if selected_theme:
            apply_sidebar_styling(THEME_OPTIONS[selected_theme])

        st.divider()

        # About section
        st.header("About")
        st.markdown("""
        This dashboard uses a CrewAI research team powered by AWS Bedrock to investigate topics.

        **The Research Team:**
        - **Researcher**: Finds cutting-edge information
        - **Reporting Analyst**: Creates detailed reports

        **Powered by:**
        - AWS Bedrock (Claude Sonnet)
        - CrewAI Framework
        - Streamlit
        """)

        # Tips section
        st.header("Tips")
        st.markdown("""
        - Be specific with your topic
        - Try: "AI trends in healthcare 2025"
        - Or: "Renewable energy market analysis"
        """)

        return selected_theme
