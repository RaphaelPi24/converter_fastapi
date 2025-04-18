import os
import shutil

from fastapi import FastAPI, WebSocket, Request, UploadFile
from starlette.responses import HTMLResponse


# Конфигурация
import os
import shutil

from fastapi import File
from fastapi import UploadFile, HTTPException, APIRouter
from redis import Redis
from rq import Queue

from converter import convert_file_to_lowercase
from tasks_example import say_hello

# подключаемся к Redis
redis_conn = Redis()
q = Queue(connection=redis_conn)

# отправляем задачу в очередь

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
from converter import convert_file_to_lowercase
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    with open("static/uploads.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
    #return TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        print('задача ставится в очередь')
        job = q.enqueue(convert_file_to_lowercase, file_path, file.filename)
        print('задача поставлена в очередь')
    return {"filename": file.filename, "message": "✅ Файл успешно загружен"}

# @app.websocket("/ws/progress")
# async def websocket_progress(websocket: WebSocket):
#     await websocket.accept()
#
#     try:
#         # Получаем от клиента длительность (в секундах)
#         data = await websocket.receive_text()
#         duration = float(data)
#
#         # Генерируем прогресс и отправляем его клиенту
#         for percent in progress_bar(duration):
#             await websocket.send_text(str(percent))
#
#         # Сообщаем о завершении
#         await websocket.send_text("done")
#
#     except Exception as e:
#         await websocket.send_text(f"error: {str(e)}")
#     finally:
#         await websocket.close()
