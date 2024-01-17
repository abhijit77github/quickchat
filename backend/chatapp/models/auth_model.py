from pydantic import BaseModel
from typing import Union, List


class UserIn(BaseModel):
    mail: str  
    name: Union[str, None] = None

class User(UserIn):
    password: str

class UserDb(UserIn):
    hashed_pass: str
    
class TokenRequest(BaseModel):
    mail: str
    password: str