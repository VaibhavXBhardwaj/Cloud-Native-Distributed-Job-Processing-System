import sys
import os
import redis

# Make sure Python can find the app module
sys.path.append("/app")

# IMPORTANT: import the task so RQ can register it
from app.tasks import process_job

# ✅ FIXED IMPORTS (no Connection in new RQ)
from rq import Worker, Queue
from redis import Redis


redis_host = os.getenv("REDIS_HOST", "redis")

# create redis connection
redis_conn = Redis(
    host=redis_host,
    port=6379,
    db=0
)

listen = ["default"]

if __name__ == "__main__":
    queues = [Queue(name, connection=redis_conn) for name in listen]

    worker = Worker(queues, connection=redis_conn)
    worker.work()