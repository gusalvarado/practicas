# ui/components/research.py
"""
Research components for displaying CrewAI results
"""

import streamlit as st
from ui.utils.helpers import extract_result_content, check_report_file_exists, create_download_filename

def display_task_outputs(result):
    """Display individual task outputs if available"""
    if hasattr(result, 'tasks_output') and result.tasks_output:
        st.header("Individual Task Results")
        for i, task_output in enumerate(result.tasks_output, 1):
            with st.expander(f"Task {i} Results", expanded=False):
                content = extract_result_content(task_output)
                st.markdown(content)
    elif hasattr(result, 'task_outputs') and result.task_outputs:
        st.header("Individual Task Results")
        for i, task_output in enumerate(result.task_outputs, 1):
            with st.expander(f"Task {i} Results", expanded=False):
                content = extract_result_content(task_output)
                st.markdown(content)

def display_research_results(result, topic):
    """Display the complete research results"""
    st.success("Investigation completed!")

    # Display the main result
    st.header("Final Report")
    main_content = extract_result_content(result)
    st.markdown(main_content)

    # Display individual task outputs
    display_task_outputs(result)

    # Check if report file was generated
    report_content = check_report_file_exists("output/report.md")
    if report_content:
        st.header("Generated Report File")
        st.markdown(report_content)

        # Provide download button
        filename = create_download_filename(topic)
        st.download_button(
            label="Download Report",
            data=report_content,
            file_name=filename,
            mime="text/markdown"
        )

def display_error(error):
    """Display error information"""
    st.error(f"An error occurred: {str(error)}")
    st.error("Please check your AWS credentials and network connection.")

    # Show detailed error info in expander
    with st.expander("Show detailed error information"):
        st.code(str(error))

def render_research_input():
    """Render the research input form"""
    st.title("Content Research Dashboard")
    st.markdown("Enter a topic and our AI research crew will investigate it thoroughly!")

    topic = st.text_input(
        "Enter a topic to investigate:",
        placeholder="e.g., AI trends in healthcare 2025",
        help="Be as specific as possible for better results",
        key="topic_input"
    )

    investigate_button = st.button("Investigate", type="primary")

    return topic, investigate_button
