import uuid
import redis
import json
from django.conf import settings


class RedisService:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def get_history(self, session_id):
      data = self.client.get(f"chat:{session_id}")
      return json.loads(data) if data else []
    
    def save_history(self, session_id, history):
      self.client.setex(f"chat:{session_id}", settings.CHAT_HISTORY_TTL, json.dumps(history))

    def generate_session_id(self):
      return str(uuid.uuid4())