from typing import Dict

from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.info_active_connections: Dict[str, WebSocket] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        self.info_active_connections[task_id] = websocket
        self.active_connections[task_id] = websocket['scope']['client'] #[0] - ip, [1] - port

    def disconnect(self, task_id: str):
        if task_id in self.active_connections:
            del self.active_connections[task_id]

    async def send_message(self, task_id: str, progress: str):
        if task_id in self.active_connections:
            await self.active_connections[task_id].send_text(f'{progress}')

    def count_active_connections(self):
        return len(self.active_connections)

    def get_info_active_connection(self):
        return self.info_active_connections