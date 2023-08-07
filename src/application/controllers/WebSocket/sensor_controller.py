from apscheduler.schedulers.base import STATE_STOPPED
from fastapi import APIRouter
from src.application.handlers.websocket_handler import WebSocketHandler
from src.domain.factories.sensor_manager_factory import SensorManagerFactory

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)

@router.websocket("/")
async def recording_handler(websocket: WebSocketHandler):
    await websocket.accept()

@router.on_event("shutdown")
def shutdown_app():
    sensor_service_factory = SensorManagerFactory()
    get_sensor_data_scheduler = sensor_service_factory.get_service().get_instance().scheduler
    if not get_sensor_data_scheduler.state == STATE_STOPPED:
        get_sensor_data_scheduler.shutdown()
