# UI Project Structure Documentation

## Modular Dashboard Architecture

The dashboard has been refactored into a modular structure for better maintainability, reusability, and testing.

### Directory Structure

```
ui/
├── __init__.py                 # Package initialization
├── dashboard.py               # Refactored main dashboard (uses modules)
├── dashboard_original.py      # Backup of original monolithic version
├── dashboard_modular.py       # Alternative entry point using app.py
├── app.py                     # Main application class
├── components/                # UI Components
│   ├── __init__.py
│   ├── sidebar.py            # Sidebar component
│   └── research.py           # Research display components
├── config/                   # Configuration
│   ├── __init__.py
│   └── settings.py           # App settings and configuration
├── styles/                   # Styling and themes
│   ├── __init__.py
│   └── themes.py             # Theme definitions and CSS
└── utils/                    # Utility functions
    ├── __init__.py
    └── helpers.py            # Helper functions
```

### Module Descriptions

#### `components/`
- **sidebar.py**: Renders the sidebar with theme selector and information
- **research.py**: Handles research input, result display, and error handling

#### `config/`
- **settings.py**: Configuration settings, page setup, and app metadata

#### `styles/`
- **themes.py**: Theme definitions, CSS styling functions for sidebar and main content

#### `utils/`
- **helpers.py**: Utility functions for result extraction, favicon loading, file handling

#### `app.py`
Main application class that orchestrates all components. Provides a clean object-oriented interface.

### Benefits of Modular Approach

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Reusability**: Components can be reused in other parts of the application
3. **Maintainability**: Easier to maintain and update individual components
4. **Testing**: Each module can be tested independently
5. **Scalability**: Easy to add new components and features
6. **Code Organization**: Clear structure makes navigation easier

### Usage Examples

#### Using the Refactored Dashboard
```bash
streamlit run ui/dashboard.py
```

#### Using the Class-based Approach
```bash
streamlit run ui/dashboard_modular.py
```

#### Importing Components
```python
from ui.components import render_sidebar, display_research_results
from ui.styles import apply_sidebar_styling
from ui.utils import extract_result_content
```

### Adding New Components

To add a new component:

1. Create a new file in `ui/components/`
2. Define your component function
3. Add it to `ui/components/__init__.py`
4. Import and use in your main application

Example:
```python
# ui/components/analytics.py
def render_analytics_panel():
    st.header("Analytics")
    # Your analytics code here

# ui/components/__init__.py
from .analytics import render_analytics_panel
```

### Customizing Themes

Add new themes in `ui/styles/themes.py`:

```python
THEMES["my_theme"] = {
    "bg_color": "#123456",
    "header_color": "#ABCDEF",
    "text_color": "#FFFFFF"
}
```

### Environment Variables

You can add environment-specific configuration in `ui/config/settings.py`:

```python
import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
```

This modular structure makes the codebase much more professional and maintainable!
