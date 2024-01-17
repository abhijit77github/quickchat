from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from ..project_constants import SECRET_KEY, ALGORITHM

class PassUtil:
    def __init__(self) -> None:
        # set haslib context
        self.pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        

    def hash_pass(self, password: str) -> str:
        hashed_pass = self.pass_context.hash(password)
        return hashed_pass
        # return password + " -- hashed"
    
    def verify_pass(self, password:str, hash_pass: str)-> bool:
        return self.pass_context.verify(password, hash_pass)
        # return self.hash_pass(password) == hash_pass


def generate_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt