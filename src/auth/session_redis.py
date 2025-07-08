from config import aio_redis_conn, SESSION_EXPIRATION


async def store_token(token: str, username: str):
    await aio_redis_conn.setex(f"session:{token}", SESSION_EXPIRATION, username)


async def get_username_from_token(token: str) -> str | None:
    return await aio_redis_conn.get(f"session:{token}")


async def delete_token(token: str):
    await aio_redis_conn.delete(f"session:{token}")
