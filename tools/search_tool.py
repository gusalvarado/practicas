import os
import json
import requests
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
  query: str = Field(..., description="Topic to search on the internet")

class SearchTool(BaseTool):
  name: str = "Search Internet"
  description: str = "Searches the internet and returns relevant results from Serper API"
  args_schema: Type[BaseModel] = SearchInput

  def _run(self, query: str) -> str:
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
        'content-type': 'application/json'
    }

    if not headers['X-API-KEY']:
        return "Error: SERPER_API_KEY not set in environment."

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json().get('organic', [])
    except Exception as e:
        return f"Error during search: {e}"

    output = []
    for r in results:
        output.append("\n".join([
            f"Title: {r['title']}",
            f"Link: {r['link']}",
            f"Snippet: {r['snippet']}",
            "---------------------------"
        ]))

    return "\n\n".join(output)