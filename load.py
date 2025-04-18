# Конфигурация
import os
import shutil

from fastapi import File
from fastapi import UploadFile, HTTPException, APIRouter

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
load_router = APIRouter()


@load_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "✅ Файл успешно загружен"}


@load_router.get("/download/{task_id}")
async def download_file(task_id: str):
    if task_id not in tasks or tasks[task_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Файл не готов или задача не найдена")

    result_filename = tasks[task_id]["result_file"]
    result_path = os.path.join(CONVERTED_FOLDER, result_filename)

    if not os.path.exists(result_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return {
        "file_path": f"/converted/{result_filename}",
        "download_url": f"/download_file/{result_filename}"
    }
