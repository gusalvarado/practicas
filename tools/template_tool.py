import re
import json
import shutil
from typing import Type
from pathlib import Path

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class ListTemplatesInput(BaseTool):
    input: str = Field(..., description="The input to be processed")

class ListTemplatesTool(BaseTool):
    name: str = "List templates"
    description: str = "List all available templates"
    args_schema: Type[BaseModel] = ListTemplatesInput

    def _run(self, input: str) -> str:
        try:
            config_path = Path("config/templates.json").resolve()

            if not config_path.exists():
                return "Error: Templates configuration file not found"

            if not str(config_path).endswith("config/templates.json"):
                return "Error: Invalid configuration file path"

            with open(config_path, "r", encoding="utf-8") as f:
                templates = json.load(f)

            return json.dumps(templates, indent=2)

        except Exception as e:
            return f"Error reading templates configuration: {str(e)}"

class CopyTemplateInput(BaseTool):
    input: str = Field(..., description="The name of the template folder to copy into the workdir")

class CopyTemplateTool(BaseTool):
    name: str = "Copy template"
    description: str = "Copy a template folder into the workdir"
    args_schema: Type[BaseModel] = CopyTemplateInput

    def _run(self, input: str) -> str:
        try:
            template_name = input.strip()

            if not re.match(r'^[a-zA-Z0-9/_.-]+$', template_name):
                return "Error: Invalid template name"
            
            if ".." in template_name or "/" in template_name or "\\" in template_name:
                return "Error: Invalid template name"

            template_base = Path("templates").resolve()
            workdir_base = Path("/tmp/").resolve()

            source = template_base / template_name
            dest = workdir_base / template_name

            source_resolved = source.resolve()
            dest_resolved = dest.resolve()

            if not str(source_resolved).startswith(str(template_base)):
                return "Error: Source path is outside of template base directory"
            if not str(dest_resolved).startswith(str(workdir_base)):
                return "Error: Destination path is outside of workdir base directory"
            if not str(source_resolved).exists():
                return f"Error: Template {template_name} not found"
            if not source_resolved.is_dir():
                return f"Error: {template_name} is not a directory"
            if dest_resolved.exists():
                return f"Error: Destination {dest_resolved} already exists"

            dest_resolved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_resolved, dest_resolved)

            return (
                f"Template '{template_name}' copied successfully to workdir.\n"
                f"You can now edit the template in the workdir and use it to create new files."
            )
        except PermissionError as e:
            return f"Error: Permission denied: {str(e)}"
        except Exception as e:
            return f"Error copying template: {str(e)}"