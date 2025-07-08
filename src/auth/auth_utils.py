from fastapi import Request, HTTPException

from auth.session_redis import get_username_from_token, store_token


async def get_current_user(request: Request) -> str:
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = await get_username_from_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    await store_token(token, username)  # обновление ттл токена в редисе

    return username.decode('utf-8')
