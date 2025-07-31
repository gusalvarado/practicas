from langchain.agents import AgentType
from langchain.chains.llm import LLMChain
from langchain.agents import initialize_agent
from core.bedrock_client import get_bedrock_client
from tools.scan import scan_nodes
from prompts.eks_agent_prompt import eks_prompt
from prompts.eks_chat_prompt import get_eks_chat_prompt

llm = get_bedrock_client()
prompt = get_eks_chat_prompt()
tools = [scan_nodes]
llm_chain = LLMChain(llm=llm, prompt=prompt)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_diagnosis(user_input):
    return agent.run(user_input)