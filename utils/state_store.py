import os
import json
import boto3
import redis
from typing import Optional

class StateStore:
    def __init__(self):
        # DynamoDB  
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table_name = os.getenv("DYNAMODB_TABLE", "ideas-table")

        # Redis
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

    #dynamo method
    def get_dynamo_state(self, key: str) -> Optional[dict]:
        response = self.dynamodb.Table(self.table_name).get_item(Key={"id": key})
        return response.get("Item", None)
    def set_dynamo_state(self, key: str, value: dict) -> None:
        self.dynamodb.Table(self.table_name).put_item(Item={"id": key, **value})

    #redis method
    def get_redis_state(self, key: str) -> Optional[str]:
        if not key:
            print(f"[REDIS] skipping get for key, key: {key} is None")
            return None
        return self.redis_client.get(key)
    
    def set_redis_state(self, key: str, value: Optional[str]) -> None:
        if not key or value is None:
            print(f"[REDIS] skipping set for key, key: {key} is None")
            return
        self.redis_client.set(key, value)

    def load_messages(self, session_id: str) -> list:
        redis_data = self.get_redis_state(session_id)
        if redis_data:
            try:
                return json.loads(redis_data)
            except Exception as e:
                print(f"[REDIS] Error loading messages: {e}")
                return []
        return []
    
    def save_messages(self, session_id: str, role: str, message: str, timestamp: str) -> None:
        messages = self.load_messages(session_id)
        messages.append({"role": role, "content": message, "timestamp": timestamp})
        self.set_redis_state(session_id, json.dumps(messages))