import redis
import os

# Connect to Redis
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

def store_in_redis(key,value,ttl=600):

    # Store a key-value pair in Redis with an optional expiry time (in seconds).
    #  default ttl is 600s or 10 minutes

    redis_client.set(key, value, ex=ttl)
def get_from_redis(key):
    # Retrieve a value from Redis by key.
    return redis_client.get(key)
