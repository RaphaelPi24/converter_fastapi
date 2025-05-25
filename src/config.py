import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=redis_conn)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = Path("/app/uploaded_files")
CONVERTED_DIR = Path("/app/converted_files")
UPLOAD_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)
TEMPLATES = Jinja2Templates(directory=STATIC_DIR)
