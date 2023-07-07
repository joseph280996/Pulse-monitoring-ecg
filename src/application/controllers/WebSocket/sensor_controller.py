from fastapi import APIRouter, WebSocket
from src.infrastructure.constants.record_operation_types import record_operation_types

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        operation_type_id = record_operation_types["STOP"]
        if data == 'start':
            operation_type_id = record_operation_types["START"]

        handler = get_record_handler(operation_type_id)
        handler()
