import json
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Optional
from .project_constants import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from .models.auth_model import UserIn
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param

bearer_scheme = HTTPBearer()

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


class ValidateToken(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        # authorization = request.headers.get("Authorization")
        # scheme, credentials = get_authorization_scheme_param(authorization)
        # if not (authorization and scheme and credentials):
        #     if self.auto_error:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        #         )
        #     else:
        #         return None
        # if scheme.lower() != "bearer":
        #     if self.auto_error:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail="Invalid authentication credentials",
        #         )
        #     else:
        #         return None
            
        self.validate_token(creds.credentials)
        return self.user
        # return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


    def validate_token(self, token: str) -> bool:
        credentials_exception = HTTPException(
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
    
    # def get_current_user(self):
    #     return self.user
