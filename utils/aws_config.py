# utils/aws_config.py
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def check_aws_credentials():
    """
    Check if AWS credentials are properly configured
    """
    try:
        # Try to create a session and check credentials
        session = boto3.Session()
        credentials = session.get_credentials()

        if credentials is None:
            raise NoCredentialsError()

        # Test if we can access bedrock
        bedrock_client = session.client('bedrock-runtime', region_name='us-east-1')

        print("AWS credentials are properly configured")
        print(f"Access Key ID: {credentials.access_key[:8]}...")
        print(f"Region: {session.region_name or 'us-east-1'}")
        return True

    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials not found or incomplete")
        print("Please configure your AWS credentials using one of these methods:")
        print("1. AWS CLI: run 'aws configure'")
        print("2. Environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("3. IAM roles (if running on EC2)")
        print("4. AWS credentials file (~/.aws/credentials)")
        return False
    except Exception as e:
        print(f"Error checking AWS configuration: {e}")
        return False

def get_bedrock_client():
    """
    Get a configured bedrock client
    """
    try:
        return boto3.client('bedrock-runtime', region_name='us-east-1')
    except Exception as e:
        print(f"Error creating Bedrock client: {e}")
        return None

if __name__ == "__main__":
    check_aws_credentials()
