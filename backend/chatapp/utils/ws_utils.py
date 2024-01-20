from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    def get_active_connection_num(self):
        return len(self.active_connections)

    async def connect(self, user_id: str,  websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id)     

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_message_by_id(self, message: str, user_id: str):
        await self.active_connections[user_id].send_json(message)

    async def broadcast(self, message: str):
        for id, ws in self.active_connections.items():
            await ws.send_json(message)
            
            
class EventMsgHandler():
    def __init__(self) -> None:
        pass
    
    def handle_event(self, event_msg: dict):
        pass