import os, json, requests
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html

class BrowserToolInput(BaseModel):
  website: str = Field(..., description="The URL to browse")

class BrowserTool(BaseTool):
  name: str = "browser_tool"
  description: str = "A tool for browsing the web"
  website: str = Field(..., description="The URL to browse")

  def _run(self, website: str) -> str:
    website = "https://chrome.browserless.io/content"
    headers = {
      "Cache-Control": "no-cache",
      "Content-Type": "application/json",
    }
    token = os.getenv("BROWSERLESS_API_KEY")
    if not token:
      raise ValueError("Missing API_KEY")
    payload = json.dumps({"url": website})

    response = requests.post(website, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    full_content = "\n\n".join([str(el) for el in elements])

    chunks = [full_content[i:i + 8000] for i in range(0, len(full_content), 8000)]
    summaries = []

    for chunk in chunks:
      summary = self.llm.invoke(
        f"""You are a principal Researcher at a big company.
        Summarize the following content, focusing on key insights and trends and ignoring fluff.
        The summary should be in markdown format.
        CONTENT:
        ---------
        {chunk}
        """
      )
      summaries.append(summary.content if hasattr(summary, "content") else summary)
      return "\n\n".join(summaries)
