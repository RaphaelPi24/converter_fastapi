import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from redis.asyncio import Redis as AsyncRedis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
aio_redis_conn = AsyncRedis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
queue_convertation = Queue("converting", connection=aio_redis_conn)
queue_file_cleanup = Queue("regular_tasks", connection=aio_redis_conn)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DB}:{POSTGRES_PORT}/{POSTGRES_DB}'

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "templates"
UPLOAD_DIR = Path("/app/uploaded_files")
CONVERTED_DIR = Path("/app/converted_files")

TEMPLATES = Jinja2Templates(directory=STATIC_DIR)

MB = 1024 * 1024  # мегабайт
MAX_UPLOAD_SIZE = 100 * MB

SESSION_EXPIRATION = 3600  # 1 час
