from fastapi import APIRouter, WebSocket
from src.application.factories.record_type_handler_factory import get_record_handler
from src.infrastructure.constants.record_operation_types import record_operation_types
from src.domain.factories.sensor_service_factory import SensorServiceFactory

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocket, service_factory = SensorServiceFactory()):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        operation_type_id = record_operation_types["STOP"]
        if data == 'start':
            operation_type_id = record_operation_types["START"]

        handler = get_record_handler(operation_type_id)
        handler()
