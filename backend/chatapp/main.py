"""Main script"""

from fastapi import Depends, FastAPI
from .routers import auth

app = FastAPI() # dependencies=[Depends(get_query_token)]
app.include_router(auth.router)

@app.get("/")
async def root():
    """doc string"""
    return {"message": "Hello Bigger Applications!"}


