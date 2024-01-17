"""Main script"""

from fastapi import Depends, FastAPI
from .routers import auth
from fastapi.security import HTTPBearer
from .dependencies import ValidateToken
from .models.auth_model import UserIn


app = FastAPI() # dependencies=[Depends(get_query_token)]
app.include_router(auth.router)
security_scheme = ValidateToken()

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


