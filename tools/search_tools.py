import os, json, requests
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class SearchToolInput(BaseModel):
  query: str = Field(..., description="The query to search for")

class SearchTool(BaseTool):
  name: str = "search_tool"
  description: str = "A tool for searching the web"
  args_schema: Type[BaseModel] = SearchToolInput

  def _run(self, query: str) -> str:
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }
    if not headers['X-API-KEY']:
      return "Missing API key"

    try:
      response = requests.post(url, headers=headers, data=payload)
      response.raise_for_status()
      results = response.json().get('organic', [])
    except Exception as e:
      return f"Error: {str(e)}"

    output = []
    for r in results:
      output.append("\n".join([
        f"Title: {r['title']}",
        f"Link: {r['link']}",
        f"Snippet: {r['snippet']}"
      ]))
    return "\n\n".join(output)