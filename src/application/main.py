import sys
sys.path.insert(0,'.')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.application.controllers.WebSocket.sensor_controller import router as ws_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(ws_router)
