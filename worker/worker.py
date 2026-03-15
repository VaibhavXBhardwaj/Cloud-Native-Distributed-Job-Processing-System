import sys
import os
import redis

# Make sure Python can find the app module
sys.path.append("/app")

# IMPORTANT: import the task so RQ can register it
from app.tasks import process_job

from rq import Worker, Queue, Connection


redis_host = os.getenv("REDIS_HOST", "redis")

redis_conn = redis.Redis(
    host=redis_host,
    port=6379,
    db=0
)

listen = ["default"]

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()