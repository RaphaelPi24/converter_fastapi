from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "templates"
UPLOAD_DIR = Path("/app/uploaded_files")
CONVERTED_DIR = Path("/app/converted_files")

TEMPLATES = Jinja2Templates(directory=STATIC_DIR)

MB = 1024 * 1024  # мегабайт
MAX_UPLOAD_SIZE = 100 * MB

SESSION_EXPIRATION = 3600  # 1 час
