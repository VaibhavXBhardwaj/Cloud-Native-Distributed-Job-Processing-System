import redis
from rq import Worker
import os

redis_host = os.getenv("REDIS_HOST", "redis")
redis_conn = redis.Redis(host=redis_host, port=6379, db=0)

worker = Worker(["default"], connection=redis_conn)
worker.work()