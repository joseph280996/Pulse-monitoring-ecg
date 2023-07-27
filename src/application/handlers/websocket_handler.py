from fastapi import Depends, WebSocket
from sqlalchemy.orm import Session
from src.domain.factories.sensor_service_factory import SensorServiceFactory
from src.infrastructure.services.database import get_db

class WebSocketHandler(WebSocket):
    __sensor_service = None
    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_received(self, websocket, data, service_factory = SensorServiceFactory(), db: Session = Depends(get_db)):
        print(f"Received message: {data}")
        if not self.__sensor_service:
            self.__sensor_service = service_factory.get_service()
        if data == 'start':
            self.__sensor_service.get_instance(db).start_reading_values()
        if data == 'stop':
            self.__sensor_service.get_instance(db).stop_reading_values()


    async def on_disconnect(self, _, close_code):
        print(f"Websocket client disconnected, code={close_code}")
        sensor_get_data_scheduler = self.__sensor_service.get_instance().scheduler;
        if sensor_get_data_scheduler.running():
            sensor_get_data_scheduler.pause()
