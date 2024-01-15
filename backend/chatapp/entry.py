"""Entry point, applications starts here"""
import uvicorn
from .main import app

def run_server():
    """Server code"""
    uvicorn.run("chatapp.main:app",  host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
