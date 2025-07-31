import os
from langchain_community.chat_models import BedrockChat

def get_bedrock_client():
    return BedrockChat(
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        model_id=os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-4-sonnet-20240620-v1:0"),
        model_kwargs={"temperature": 0.0, "max_tokens": 1000}
    )