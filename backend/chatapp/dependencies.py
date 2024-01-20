import json
from fastapi import Depends, HTTPException, status, Header, WebSocketException, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Optional
from .project_constants import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from .models.auth_model import UserIn
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param

bearer_scheme = HTTPBearer()

class GenException(Exception):
    def __init__(self, status_code: int, detail: str, headers: str) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
        super().__init__(self.detail)
    

class Getdb:
    def __init__(self) -> None:
        self.file_name = 'my_db.json'
        self.data = {}
    
    def write_data(self, data):
        with open(self.file_name, "w", encoding='utf-8') as f:
            json.dump(data, f)
        self.data = data

    def read_data(self):
        try:
            with open(self.file_name, "r", encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            self.data = {}
            return {}

class BaseTokenValidation:
   def validate_token(self, token: str) -> bool:
        credentials_exception = GenException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("name")
            mail: str = payload.get("mail")
            if mail is None:
                raise credentials_exception
            self.user = UserIn(name=username, mail=mail)
        except JWTError:
            raise credentials_exception

class ValidateToken(HTTPBearer, BaseTokenValidation):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        try:
            self.validate_token(creds.credentials)            
            return self.user
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )
        
class WsTokenValidation(BaseTokenValidation):
    def __call__(self, ws: WebSocket) ->Optional[UserIn]: # authorization: Annotated['str', Header()]        
        scheme, cred = ws.headers.get('authorization').split(' ')
        if scheme.lower() != "bearer":
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid authentication credentials",
            )
        self.token = cred
        try:
            self.validate_token(self.token)            
            return self.user
        except Exception as e:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid authentication credentials",
            )
        
            
