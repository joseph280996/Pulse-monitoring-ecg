from fastapi import APIRouter
from src.application.handlers.websocket_handler import WebSocketHandler

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocketHandler):
    await websocket.accept()

