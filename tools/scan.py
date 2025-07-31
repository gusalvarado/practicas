import subprocess
from langchain.tools import tool

@tool
def scan_nodes(tool_input: str) -> str:
    """Scan the EKS cluster and list nodes"""
    try:
        return subprocess.check_output(["kubectl", "get", "nodes"], text=True)
    except subprocess.CalledProcessError as e:
        return f"Error scanning nodes: {e}"