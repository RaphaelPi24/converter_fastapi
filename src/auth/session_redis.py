from config import aio_redis_conn, SESSION_EXPIRATION


def store_token(token: str, username: str):
    aio_redis_conn.setex(f"session:{token}", SESSION_EXPIRATION, username)


def get_username_from_token(token: str) -> str | None:
    return aio_redis_conn.get(f"session:{token}")


def delete_token(token: str):
    aio_redis_conn.delete(f"session:{token}")
