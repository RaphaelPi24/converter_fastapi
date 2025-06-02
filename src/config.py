import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
queue_convertation = Queue("converting", connection=redis_conn)
queue_file_cleanup = Queue("regular_tasks", connection=redis_conn)
aio_redis_conn = AsyncRedis.from_url("redis://redis:6379") # надо прокинуть в .env

DATABASE_URL = "postgresql://converter_user:converter_password@converter_db:5432/converter_db"
#DATABASE_URL=f'postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}'


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "templates"
UPLOAD_DIR = Path("/app/uploaded_files")
CONVERTED_DIR = Path("/app/converted_files")

TEMPLATES = Jinja2Templates(directory=STATIC_DIR)

MB = 1024 * 1024  # мегабайт
MAX_UPLOAD_SIZE = 100 * MB  # 10 MB

SESSION_EXPIRATION = 3600  # 1 час
MAX_AGE_COOKIE = 3600 * 24  # сутки
