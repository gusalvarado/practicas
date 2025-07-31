from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def get_eks_chat_prompt():
    system_template = """
    You are a kubernetes and AWS EKS expert assistant.
    Your job is to help DevOps engineers to understand the state of the EKS cluster, diagnose issues, and provide recommendations.

    You can use tools such as `kubectl` to get node, pod, and event information.
    Always provide:
    - A clear summary of the cluster health
    - Explanation of any issues found
    - Actionable recommendations for next steps
    - Use short bullet points and markdown formatting

    Respond concisely and use technical terms when appropriate.
    """

    human_template = "{input}"

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])