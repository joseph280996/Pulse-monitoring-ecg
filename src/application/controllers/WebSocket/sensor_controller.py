from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocket):
    await websocket.accept()
