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
    try:
        if isinstance(value, dict):
            # Convert dictionary to string before storing
            value = str(value)
        redis_client.set(key, value, ex=ttl)
    except Exception as ex:
        print(f"Error storing in redis {ex}")
        return None
def get_from_redis(key):
    # Retrieve a value from Redis by key.
    try:
        redis_value = redis_client.get(key)
        if redis_value is not None:
            # Convert string back to dictionary if needed
            try:
                redis_value = eval(redis_value)
            except:
                pass
            return redis_value
    except Exception as ex:
        print(f"Error retrieving from redis {ex}")
        return None
       
