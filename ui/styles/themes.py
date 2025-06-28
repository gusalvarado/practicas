# ui/styles/themes.py
"""
Theme definitions and styling functions for the Streamlit dashboard
"""

import streamlit as st

# Color theme definitions
THEMES = {
    "dark_blue": {
        "bg_color": "#2E4057",
        "header_color": "#FFD700",
        "text_color": "#E8E8E8"
    },
    "green": {
        "bg_color": "#1B5E20",
        "header_color": "#C8E6C9",
        "text_color": "#E8F5E8"
    },
    "purple": {
        "bg_color": "#4A148C",
        "header_color": "#E1BEE7",
        "text_color": "#F3E5F5"
    },
    "orange": {
        "bg_color": "#E65100",
        "header_color": "#FFF3E0",
        "text_color": "#FFF8E1"
    },
    "red": {
        "bg_color": "#B71C1C",
        "header_color": "#FFCDD2",
        "text_color": "#FFEBEE"
    },
    "teal": {
        "bg_color": "#004D40",
        "header_color": "#B2DFDB",
        "text_color": "#E0F2F1"
    }
}

# Theme display names
THEME_OPTIONS = {
    "Dark Blue": "dark_blue",
    "Forest Green": "green",
    "Purple": "purple",
    "Orange": "orange",
    "Red": "red",
    "Teal": "teal"
}

def apply_sidebar_styling(color_theme="dark_blue"):
    """Apply custom CSS styling to the sidebar"""
    theme = THEMES.get(color_theme, THEMES["dark_blue"])

    css = f"""
    <style>
        /* Sidebar background color */
        .css-1d391kg {{
            background-color: {theme["bg_color"]};
        }}

        /* Alternative selector for sidebar */
        .stSidebar > div:first-child {{
            background-color: {theme["bg_color"]};
        }}

        /* Sidebar text color */
        .css-1d391kg .markdown-text-container {{
            color: {theme["text_color"]};
        }}

        /* Sidebar headers */
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {{
            color: {theme["header_color"]};
        }}

        /* Sidebar links and text */
        .css-1d391kg p, .css-1d391kg li {{
            color: {theme["text_color"]};
        }}

        /* For newer Streamlit versions */
        section[data-testid="stSidebar"] {{
            background-color: {theme["bg_color"]};
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {theme["header_color"]};
        }}

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li {{
            color: {theme["text_color"]};
        }}

        /* Emoji styling in sidebar */
        section[data-testid="stSidebar"] .markdown-text-container {{
            color: {theme["text_color"]};
        }}

        /* Sidebar input widgets */
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stSlider label {{
            color: {theme["text_color"]} !important;
        }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

def apply_main_content_styling():
    """Apply styling to main content area"""
    st.markdown("""
    <style>
        /* Main content area improvements */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Better spacing for headers */
        .stHeader {
            margin-bottom: 1rem;
        }

        /* Improve button styling */
        .stButton > button {
            background-color: #0066CC;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #0052A3;
        }

        /* Success message styling */
        .stSuccess {
            border-radius: 5px;
        }

        /* Download button styling */
        .stDownloadButton > button {
            background-color: #28A745;
            color: white;
            border: none;
            border-radius: 5px;
        }

        .stDownloadButton > button:hover {
            background-color: #218838;
        }
    </style>
    """, unsafe_allow_html=True)
