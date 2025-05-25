from fastapi import Request, HTTPException

from auth.session_redis import get_username_from_token


def get_current_user(request: Request) -> str:
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = get_username_from_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return username
