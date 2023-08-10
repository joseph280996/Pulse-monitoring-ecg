from apscheduler.schedulers.base import STATE_STOPPED
from fastapi import Depends, WebSocket
from sqlalchemy.orm import Session
from src.domain.managers.sensor_manager import EcgSensorManager
from src.infrastructure.services.database import get_db


class WebSocketHandler(WebSocket):
    __sensor_service = None

    def get_sensor_service(self, db: Session = Depends(get_db)):
        service_factory = EcgSensorManager()
        if not self.__sensor_service:
            self.__sensor_service = service_factory.get_service().get_instance(db)
        return self.__sensor_service

    async def on_connect(self, websocket):
        await websocket.accept()

    async def send_sensor_message(self, websocket: WebSocket):
        service = self.get_sensor_service()
        data = service.get_data()
        await websocket.send_json(data)

    async def on_received(self, websocket, data):
        print(f"Received message: {data}")
        service = self.get_sensor_service()
        if data == "start":
            service.start_reading_values()
        if data == "stop":
            service.stop_reading_values()

    async def on_disconnect(self, _, close_code):
        print(f"Websocket client disconnected, code={close_code}")
        sensor_get_data_scheduler = self.__sensor_service.get_instance().scheduler
        if (
            sensor_get_data_scheduler.running
            and not sensor_get_data_scheduler.state == STATE_STOPPED
        ):
            sensor_get_data_scheduler.pause()
