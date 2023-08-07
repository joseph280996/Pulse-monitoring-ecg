from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends
from sqlalchemy.orm import Session
from src.domain.factories.sensor_manager_factory import SensorManagerFactory
from src.infrastructure.services.database import get_db


class SendSensorValueService():
    def __init__(self, websocket, db: Session = Depends(get_db)):
        self.__scheduler = AsyncIOScheduler()
        self.__sensor_service_factory = SensorManagerFactory().get_service().get_instance(db)
        self.websocket = websocket

    def start_sending_sensor_values(self):
        
