import random
from datetime import datetime
from time import sleep
from typing import Sequence
from models.stoppable_thread import StoppableThread
from models.recorded_datum import RecordedData
from fastapi import Depends
from sqlalchemy.orm import Session
from domain.repositories.record_repository import RecordRepository
from infrastructure.services.database import get_db

class EcgSensorService:
    __instance = None

    def get_instance(self):
        if not EcgSensorService.__instance:
            EcgSensorService.__instance = EcgSensorService()
        return EcgSensorService.__instance

    def __init__(self, db:Session = Depends(get_db)):
        self.__data: Sequence[RecordedData] = []
        self.__db = db
        self.__record_repository = RecordRepository.get_instance(self.__db)

    def start_reading_values(self):
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
        )
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.__reading_ecg_thread.stop()

        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")

        self.__record_repository.create(self.__data)
        self.__data.clear()

    def __reading_ecg_sensor_data(self, stop_event):
        while not stop_event.is_set():
            if len(self.__data) >= 1000:
                self.__record_repository.create(self.__data)
                self.__data.clear()
            current_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            self.__data.append(
                RecordedData(
                    time_stamp=current_timestamp,
                    data=random.random,
                )
            )
            sleep(0.01)
