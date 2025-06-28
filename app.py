# ui/app.py
"""
Main application logic for the research dashboard
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from crew import ContentCrew

import streamlit as st

from ui.config.settings import configure_page, RESEARCH_CONFIG
from ui.components.sidebar import render_sidebar
from ui.components.research import render_research_input, display_research_results, display_error
from ui.styles.themes import apply_sidebar_styling, apply_main_content_styling

class ResearchDashboard:
    """Main dashboard application class"""

    def __init__(self):
        self.crew = None

    def setup(self):
        """Setup the dashboard"""
        configure_page()
        apply_main_content_styling()
        # Apply default sidebar styling
        apply_sidebar_styling("dark_blue")

    def run(self):
        """Run the main dashboard application"""
        self.setup()

        # Render sidebar and get selected theme
        selected_theme = render_sidebar()

        # Render main content
        topic, investigate_button = render_research_input()

        # Handle investigation
        if investigate_button:
            if topic and topic.strip():
                self._run_investigation(topic.strip())
            else:
                st.warning("Please enter a topic to investigate.")

    def _run_investigation(self, topic):
        """Run the research investigation"""
        # Validate topic length
        if len(topic) > RESEARCH_CONFIG["max_topic_length"]:
            st.error(f"Topic is too long. Please limit to {RESEARCH_CONFIG['max_topic_length']} characters.")
            return

        with st.spinner(RESEARCH_CONFIG["spinner_text"]):
            inputs = {'topic': topic}

            try:
                # Initialize crew if not already done
                if not self.crew:
                    self.crew = ContentCrew().crew()

                # Run the investigation
                result = self.crew.kickoff(inputs=inputs)

                # Display results
                display_research_results(result, topic)

            except Exception as e:
                display_error(e)

def main():
    """Main entry point"""
    dashboard = ResearchDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
