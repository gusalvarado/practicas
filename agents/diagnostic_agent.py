from tabnanny import verbose
from tools.scan import scan_nodes
from tools.bedrock import get_bedrock_client
from langgraph.prebuilt import create_react_agent
from prompts.eks_chat_prompt import get_eks_chat_prompt

model = get_bedrock_client()
tools = [scan_nodes]
prompt = get_eks_chat_prompt()

agent_executor = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt
)

def run_diagnosis(user_input: str) -> str:
    return agent_executor.invoke({"input": user_input})