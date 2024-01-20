"""Main script"""

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from .routers import auth
from fastapi.security import HTTPBearer
from .dependencies import ValidateToken
from .models.auth_model import UserIn
from .utils.ws_utils import ConnectionManager
from .dependencies import WsTokenValidation
import json


app = FastAPI() # dependencies=[Depends(get_query_token)]
app.include_router(auth.router)
security_scheme = ValidateToken()
ws_security_scheme = WsTokenValidation()
ws_con_manager = ConnectionManager()


@app.get("/")
async def root():
    """doc string"""
    return {"message": "Hello Bigger Applications!"}

@app.get("/private_1/", dependencies=[Depends(security_scheme)])
async def private_route_generic():
    """doc string"""
    return {"message": f"Hello this is a private route, generic"}
    
@app.get("/private_2/")
async def private_route(user: UserIn = Depends(security_scheme)):
    """doc string"""
    return {"message": f"Hello {user.mail}"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: UserIn = Depends(ws_security_scheme)):    
    await ws_con_manager.connect(user.mail, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
