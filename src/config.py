import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # не работает
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue_convertation = Queue("converting", connection=redis_conn)
queue_file_cleanup = Queue("regular_tasks", connection=redis_conn)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "templates"
UPLOAD_DIR = Path("/app/uploaded_files")
CONVERTED_DIR = Path("/app/converted_files")

TEMPLATES = Jinja2Templates(directory=STATIC_DIR)

# class Config:
#     redis: RedisConfig
#     paths: PathConfig
#     
#     
# config = Config()
# config.redis.host
# config.paths.upload
