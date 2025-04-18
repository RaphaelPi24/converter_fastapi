# Конфигурация
import asyncio
import shutil
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import FileResponse
from redis import Redis
from rq import Queue
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from converter import CONVERTED_FOLDER, count_characters_in_file, from_number_to_sec, convert_file, \
    get_converted_filename
from generator import progress_bar

redis_conn = Redis()
q = Queue(connection=redis_conn)

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()


def windows_to_wsl_path(windows_path: str) -> str:
    return windows_path.replace("C:\\", "/mnt/c/").replace("\\", "/")


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

        print('Файл загружен, считаем длину...')
        char_count = count_characters_in_file(file_path)
        fake_duration = from_number_to_sec(char_count)

        converted_filename = get_converted_filename(file.filename, conversionType)

        print('Ставим задачу в очередь...')
        unix_style_path = windows_to_wsl_path(str(file_path))
        job = q.enqueue(convert_file, unix_style_path, file.filename, conversionType)

    return {
        "filename": file.filename,
        "converted_filename": converted_filename,
        "duration": fake_duration,
        "message": "✅ Файл успешно загружен"
    }

#
# @app.websocket("/ws/progress/{filename}")
# async def websocket_progress(websocket: WebSocket, filename: str):
#     await websocket.accept()
#     try:
#         while True:
#             progress = redis_conn.get(f"progress:{filename}")
#             if progress:
#                 percent = int(progress.decode())
#                 await websocket.send_text(str(percent))
#                 if percent >= 100:
#                     break
#             await asyncio.sleep(0.5)
#         await websocket.send_text("done")
#     except Exception as e:
#         await websocket.send_text(f"error: {str(e)}")
#     finally:
#         await websocket.close()
@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        duration = float(data)

        for percent in progress_bar(duration - 8):
            await websocket.send_text(str(percent))

        await websocket.send_text("done")
    except Exception as e:
        await websocket.send_text(f"error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = CONVERTED_FOLDER / filename
    if not file_path.exists():
        return {"error": "Файл не найден"}
    return FileResponse(file_path, filename=filename, media_type='application/octet-stream')
