# middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


# config.py
MB = 1024 * 1024 # мегабайт
MAX_UPLOAD_SIZE = 10 * MB  # 10 MB

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("content-length"):
            content_length = int(request.headers["content-length"])
            if content_length > MAX_UPLOAD_SIZE:
                return JSONResponse(
                    status_code=413,
                    content={"detail": f"Размер файла превышает лимит {MAX_UPLOAD_SIZE // MB} МБ"},
                )
        return await call_next(request)
