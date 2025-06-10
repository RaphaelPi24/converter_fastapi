import shutil
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import FastAPI, Form, UploadFile, File
from fastapi import Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi_limiter import FastAPILimiter
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.websockets import WebSocket

from auth.auth_utils import get_current_user
from auth.routers import router as auth_router
from config import UPLOAD_DIR, CONVERTED_DIR, TEMPLATES, queue_convertation, queue_file_cleanup, aio_redis_conn
from converters.convertor import Selector
from converters.utils import get_converted_filename, convert_file
from fake_progress import async_progress_bar, from_number_to_sec
from file_cleanup import cleanup_files
from middleware import LimitUploadSizeMiddleware

UPLOAD_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await FastAPILimiter.init(aio_redis_conn)
    yield
    await FastAPILimiter.close()
    await aio_redis_conn.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(LimitUploadSizeMiddleware)
app.include_router(auth_router)


# --- Роуты ---
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        if "expired" in str(exc.detail).lower():
            return TEMPLATES.TemplateResponse("expired_token.html", {"request": request}, status_code=401)
        return TEMPLATES.TemplateResponse("not_authenticated.html", {"request": request}, status_code=401)
    return HTMLResponse(f"{exc.status_code} - {exc.detail}", status_code=exc.status_code)


@app.get("/", response_class=HTMLResponse)
async def form(request: Request, current_user: str = Depends(get_current_user)):
    format_pairs = Selector.get_all_supported_pairs()
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
    new_name = get_converted_filename(file.filename, conversion_type)
    job = queue_convertation.enqueue(convert_file, str(file_path), file.filename, conversion_type)  # job?
    job2 = queue_file_cleanup.enqueue_in(
        timedelta(seconds=300),
        cleanup_files,
        args=(file_path,)
    )
    job3 = queue_file_cleanup.enqueue_in(
        timedelta(seconds=200),
        cleanup_files,
        args=(file_path,) # путь + имя
    )

    return {
        "filename": file.filename,
        "converted_filename": get_converted_filename(file.filename, conversion_type),
        "message": "✅ Файл успешно загружен"
    }


@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        try:
            duration = from_number_to_sec(data)
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


@app.api_route("/download/{filename}", methods=["GET", "HEAD"])
def download_file(filename: str):
    """ HEAD - автопроверка наличия файла и если успешно сразу же ставится job2
    БОЛЬШИЙ ТАЙМАУТ ПРИ HEAD
        GET - скачивание файла и тоже ставится job2
    """
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        return HTMLResponse(content="Файл не найден", status_code=404)

    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")
