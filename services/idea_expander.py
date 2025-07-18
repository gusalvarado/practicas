from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel

from tools.search_tool import SearchTool
from tools.browser_tool import BrowserTool

from langchain_core.tools import Tool
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class IdeaExpander:
  def __init__(self, llm: BaseChatModel = None):
    self.llm = llm or ChatBedrock(
      model_id="amazon.titan-text-lite-v1",
      region_name="us-east-1"
    )
    self.tools: list[Tool] = [SearchTool(), BrowserTool()]

  def expand(self, idea: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
      ("system", "You are a startup strategist, Expand ideas into startup-level pitch summaries."),
      ("human", "Expand this idea into a compeling concept: {idea}")
    ])
    chain: Runnable = prompt | self.llm | StrOutputParser()
    return chain.invoke({"idea": idea})