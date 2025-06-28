# ui/utils/helpers.py
"""
Utility functions for the dashboard
"""

import os
from PIL import Image

def extract_result_content(result):
    """Extract content from CrewAI result object"""
    if hasattr(result, 'raw') and result.raw:
        return result.raw
    elif hasattr(result, 'output') and result.output:
        return result.output
    elif hasattr(result, 'result') and result.result:
        return result.result
    else:
        return str(result)

def load_favicon():
    """Load favicon with fallback options"""
    favicon_options = [
        ('favicon.ico', 'ICO'),
        ('favicon.png', 'PNG'),
        ('favicon-96x96.png', 'PNG'),
        ('favicon.svg', 'SVG')
    ]

    for filename, format_type in favicon_options:
        try:
            favicon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'favicon', filename)
            if os.path.exists(favicon_path):
                if format_type == 'SVG':
                    # For SVG, you might want to use a different approach
                    # SVG support depends on Streamlit version
                    continue
                else:
                    return Image.open(favicon_path)
        except Exception as e:
            continue

    # Fallback to emoji
    return "🔍"

def create_download_filename(topic, suffix="report"):
    """Create a safe filename for downloads"""
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_')
    return f"{safe_topic}_{suffix}.md"

def check_report_file_exists(report_path="output/report.md"):
    """Check if the report file exists and return its content"""
    if os.path.exists(report_path):
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return None
    return None
