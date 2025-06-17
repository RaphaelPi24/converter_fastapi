from config import redis_conn, SESSION_EXPIRATION


class TokenManager:
    def __init__(self, token: str):
        self.token = self.get_key(token)

    def get_key(self, token: str) -> str:
        return f'session:{token}'

    def store_token(self, username: str) -> None:
        redis_conn.setex(self.token, SESSION_EXPIRATION, username)

    def get_username_from_token(self) -> bytes | None:
        return redis_conn.get(self.token)

    def delete_token(self) -> None:
        redis_conn.delete(self.token)
