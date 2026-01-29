from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from dotenv import load_dotenv

load_dotenv()

from app.database import engine
from app.models import all_models
from app.api.router import api_router
from app.core.socket import manager
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

# Ensure uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Ensure tables are created
all_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Analyzer AI", version="1.0.0")

# Standard CORS handling - using explicit origins to allow credentials
allow_origins_list = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

# Add dynamic origins from env
if os.getenv("BACKEND_CORS_ORIGINS"):
    origins_env = os.getenv("BACKEND_CORS_ORIGINS").split(",")
    allow_origins_list.extend([origin.strip() for origin in origins_env])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

app.include_router(api_router, prefix="/api/v1")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

