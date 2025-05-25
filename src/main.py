import shutil

from fastapi import FastAPI, Form, UploadFile, File
from fastapi import Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from rq import Repeat
from starlette.websockets import WebSocket

from auth.auth_utils import get_current_user
from auth.routers import router as auth_router
from config import UPLOAD_DIR, CONVERTED_DIR, TEMPLATES, q
from convert_code.interface import UniversalInterface
from convert_code.utils import get_converted_filename, convert_file
from fake_progress import async_progress_bar, from_number_to_sec
from file_cleanup import cleanup_files
from middleware import LimitUploadSizeMiddleware

# --- Инициализация ---
app = FastAPI()
app.add_middleware(LimitUploadSizeMiddleware)
app.include_router(auth_router)

job = q.enqueue(cleanup_files, repeat=Repeat(times=100_000, interval=900))
# --- Роуты ---

@app.get("/", response_class=HTMLResponse)
async def form(request: Request, current_user: str = Depends(get_current_user)):
    format_pairs = UniversalInterface.get_all_supported_pairs()
    return TEMPLATES.TemplateResponse("index.html", {
        "request": request,
        "format_pairs": format_pairs,
        "current_user": current_user  # имя юзера из токена
    })


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), conversion_type: str = Form(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    converted_filename = get_converted_filename(file.filename, conversion_type)
    job = q.enqueue(convert_file, str(file_path), file.filename, conversion_type)

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
