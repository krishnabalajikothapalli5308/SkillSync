import json
import os
from redis import Redis
from redis.exceptions import RedisError

_client = None

def get_redis():
    global _client
    if _client is None:
        _client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"),
                                 decode_responses=True, socket_connect_timeout=0.25)
    return _client

def cache_get(key: str):
    try:
        value = get_redis().get(key)
        return json.loads(value) if value else None
    except RedisError:
        return None

def cache_set(key: str, value, ttl: int = 60):
    try:
        get_redis().setex(key, ttl, json.dumps(value, default=str))
    except RedisError:
        pass

def cache_delete_pattern(pattern: str):
    try:
        client = get_redis()
        for key in client.scan_iter(match=pattern, count=100):
            client.delete(key)
    except RedisError:
        pass

def redis_status() -> str:
    try:
        get_redis().ping()
        return "connected"
    except RedisError:
        return "unavailable (API continues without cache)"
