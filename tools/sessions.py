import os
import redis
import json
from datetime import datetime

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
SESSION_TTL = 86400  # 24 hours in seconds

_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def set_session(session_id: str, user_info: dict):
    key = f"session:{session_id}"
    payload = {
        "user_info": user_info,
        "created_at": datetime.utcnow().isoformat()
    }
    try:
        _redis.setex(key, SESSION_TTL, json.dumps(payload))
    except redis.RedisError as e:
        print(f"[Redis] Error setting session: {e}")

def get_session(session_id: str):
    key = f"session:{session_id}"
    try:
        value = _redis.get(key)
        if value is None:
            return None
        data = json.loads(value)
        return data.get("user_info")
    except (redis.RedisError, json.JSONDecodeError) as e:
        print(f"[Redis] Error getting session: {e}")
        return None

def delete_session(session_id: str):
    key = f"session:{session_id}"
    try:
        _redis.delete(key)
    except redis.RedisError as e:
        print(f"[Redis] Error deleting session: {e}")