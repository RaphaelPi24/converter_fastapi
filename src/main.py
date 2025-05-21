import shutil
from datetime import datetime, timezone
from pathlib import Path
from rq_scheduler import Scheduler
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue
from starlette.websockets import WebSocket

from convert_code.interface import UniversalInterface
from convert_code.utils import get_converted_filename, convert_file
from fake_progress import async_progress_bar, from_number_to_sec
from file_cleanup import cleanup_files
from middleware import LimitUploadSizeMiddleware

# --- Инициализация ---
app = FastAPI()
app.add_middleware(LimitUploadSizeMiddleware) # ограничение на загрузку файлов
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploaded_files"
CONVERTED_DIR = BASE_DIR / "converted_files"

UPLOAD_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)

TEMPLATES = Jinja2Templates(directory=STATIC_DIR)

# --- Redis + RQ ---
redis_conn = Redis(host="redis", port=6379)
q = Queue(connection=redis_conn)


scheduler = Scheduler(connection=redis_conn)

# Планировать запуск каждые 15 минут
scheduler.schedule(
    scheduled_time=datetime.now(timezone.utc),
    func=cleanup_files,
    args=[[Path("../uploaded_files"), Path("../converted_files")]],
    interval=310,  # каждые 900 секунд (15 минут)
    repeat=None # повтор бесконечно, а не определенное количество раз
)

# --- Роуты ---
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    format_pairs = UniversalInterface.get_all_supported_pairs()
    return TEMPLATES.TemplateResponse("index.html", {
        "request": request,
        "format_pairs": format_pairs
    })


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), conversionType: str = Form(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    converted_filename = get_converted_filename(file.filename, conversionType)
    job = q.enqueue(convert_file, str(file_path), file.filename, conversionType)

    return {
        "filename": file.filename,
        "converted_filename": converted_filename,
        "message": "✅ Файл успешно загружен"
    }


@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        try:
            duration = from_number_to_sec(int(data))
        except ValueError:
            await websocket.send_text("error: invalid number")
            await websocket.close()
            return

        async for percent in async_progress_bar(duration):
            await websocket.send_text(str(percent))
        await websocket.send_text("done")

    except Exception as e:
        await websocket.send_text(f"error: {str(e)}")
    finally:
        await websocket.close()


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        return HTMLResponse(content="Файл не найден", status_code=404)
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")
