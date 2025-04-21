# Конфигурация
import shutil
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import FileResponse
from redis import Redis
from rq import Queue
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket

from converter import CONVERTED_FOLDER, convert_file, \
    get_converted_filename
from fake_progress import async_progress_bar, from_number_to_sec

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

BASE_DIR = Path(__file__).resolve().parent  # Абсолютный путь к текущей папке (обычно /app в Docker)
CONVERTED_DIR = BASE_DIR / "converted_files"

app = FastAPI()


# def windows_to_wsl_path(windows_path: str) -> str:
#     return windows_path.replace("C:\\", "/mnt/c/").replace("\\", "/")


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    with open("static/uploads.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        conversionType: str = Form(...)
):
    print('1111')
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
        data = await websocket.receive_text()  # длина
        print(data)
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


# @app.get("/download/{filename}")
# async def download_file(filename: str):
#     file_path = CONVERTED_FOLDER / filename
#     if not file_path.exists():
#         return {"error": "Файл не найден"}
#     return FileResponse(file_path, filename=filename, media_type='application/octet-stream')

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = CONVERTED_DIR / filename

    print("🧭 Current working dir:", Path.cwd())  # рабочая директория
    print("🔍 Looking for file at:", file_path)  # полный путь до файла

    if not file_path.exists():
        return JSONResponse(content={"error": "Файл не найден"}, status_code=404)

    return FileResponse(path=file_path, media_type="application/octet-stream", filename=filename)