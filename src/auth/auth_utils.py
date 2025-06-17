from fastapi import Request, HTTPException

from auth.session_redis import TokenManager


def get_current_user(request: Request) -> str:
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = TokenManager(token)
    username = token.get_username_from_token()
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    token.store_token(username.decode("utf-8"))  # обновление ттл токена в редисе

    return username.decode("utf-8")
