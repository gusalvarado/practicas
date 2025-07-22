import re
from typing import Type
from pathlib import Path
from utils.s3_uploader import upload_file

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class FileToolInput(BaseTool):
    data: str = Field(..., description="The data to be processed")

class FileTool(BaseTool):
    name: str = "Write to file"
    description: str = "Writes content to a file inside the give directory"
    args_schema: Type[BaseModel] = FileToolInput

    def _run(self, data):
        try:
            if "|" not in data:
                return "Error: Input must contain a pipe (|) to separate the file path and the content"
            path, content = data.split("|", 1)
            path = path.strip().replace("\n", "").replace(" ", "").replace("`", "")

            if not re.match(r'^[a-zA-Z0-9/_.-]+$', path):
                return "Error: Invalid characters in the file"

            working_dir = Path("/tmp/").resolve()

            if path.startswith("/tmp"):
                relative_path = path[10:]
            elif path.startswith("./"):
                relative_path = path[2:]
            elif path.startswith("/"):
                return "Error: Absolute paths are not allowed"
            else:
                relative_path = path
            
            if ".." in relative_path or relative_path.startswith("/"):
                return "Error: relative path with .. is not allowed"

            target_path = working_dir / relative_path
            
            try:
                resolved_path = target_path.resolve()
                if not str(resolved_path).startswith(str(working_dir)):
                    return "Error: Path resolves outside of working directory"
            except Exception as e:
                return "Error: Path resolves outside of working directory {e}"
            
            allowed_extensions = {".txt", ".md", ".json", ".yaml", ".yml", ".csv", ".tsv", ".html", ".css", ".js", ".py", ".sh", ".bat", ".ps1", ".psm1", ".psd1", ".ps1xml", ".pssc", ".psrc", ".psrcxml", ".psrcpsd1", ".psrcpsd2", ".psrcpsd3", ".psrcpsd4", ".psrcpsd5", ".psrcpsd6", ".psrcpsd7", ".psrcpsd8", ".psrcpsd9", ".psrcpsd10"}
            if resolved_path.suffix.lower() not in allowed_extensions:
                return f"Error: Invalid file extension. Allowed extensions are: {', '.join(allowed_extensions)}"

            resolved_path.parent.mkdir(parents=True, exist_ok=True)

            with open(resolved_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"File {resolved_path} created successfully"

        except PermissionError as e:
            return f"Error: Permission denied: {str(e)}"
        except ValueError as e:
            return f"Error: Invalid file path: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
