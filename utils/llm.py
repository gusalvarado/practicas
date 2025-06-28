from crewai import LLM

# Check AWS credentials on import

llm = LLM(
    model='bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0',
    aws_region_name='us-east-1',
    aws_access_key_id=None,  # Will use default AWS credentials
    aws_secret_access_key=None,  # Will use default AWS credentials
    max_tokens=1024,
    temperature=0.7,
    top_p=0.9
)
