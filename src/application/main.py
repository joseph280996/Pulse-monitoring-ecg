import sys
sys.path.insert(0,'.')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.application.controllers.REST import record_data_controller, diagnosis_notify_controller

origins = ["http://localhost", "http://localhost:8080"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(record_data_controller.router)
app.include_router(diagnosis_notify_controller.router)
