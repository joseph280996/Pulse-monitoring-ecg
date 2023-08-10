from apscheduler.schedulers.base import STATE_STOPPED
from fastapi import APIRouter
from src.application.handlers.websocket_handler import WebSocketHandler
from src.domain.managers.sensor_manager import EcgSensorManager

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocketHandler):
    """WebSocket Controller

    Create an instance of the WebSocket Handler and run it to receive any incoming message
    """
    await websocket.accept()

@router.on_event("shutdown")
def shutdown_app():
    """On Shutdown clean up function.

    This function will listen to the shutdown event and perform clean up on any loop scheduler.
    """
    sensor_manager = EcgSensorManager.get_instance()
    get_sensor_data_scheduler = sensor_manager.scheduler
    if not get_sensor_data_scheduler.state == STATE_STOPPED:
        get_sensor_data_scheduler.shutdown()
