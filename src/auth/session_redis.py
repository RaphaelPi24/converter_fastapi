# session_redis.py

from config import redis_conn

SESSION_EXPIRATION = 3600  # 1 час


def store_token(token: str, username: str):
    redis_conn.setex(f"session:{token}", SESSION_EXPIRATION, username)


def get_username_from_token(token: str) -> str | None:
    return redis_conn.get(f"session:{token}")


def delete_token(token: str):
    redis_conn.delete(f"session:{token}")
