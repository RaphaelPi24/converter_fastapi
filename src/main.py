import shutil
from pathlib import Path

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket
from redis import Redis
from rq import Queue

from convert_code.interface import UniversalInterface
from convert_code.utils import get_converted_filename
from fake_progress import async_progress_bar, from_number_to_sec

# --- Инициализация ---
app = FastAPI()

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
    job = q.enqueue("convert_code.utils.convert_file", str(file_path), file.filename, conversionType)

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
