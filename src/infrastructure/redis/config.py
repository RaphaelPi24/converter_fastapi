import os

from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue_convertation = Queue("converting", connection=redis_conn)
queue_file_cleanup = Queue("regular_tasks", connection=redis_conn)
aio_redis_conn = AsyncRedis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
