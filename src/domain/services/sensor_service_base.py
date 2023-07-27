import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends
from sqlalchemy.orm import Session
from time import sleep, time
from typing import Sequence, Optional
from src.domain.models.record_session import RecordSession
from src.domain.repositories.record_repository import RecordRepository
from src.domain.repositories.record_session_repository import RecordSessionRepository
from src.infrastructure.services.database import get_db
from models.recorded_datum import RecordedData


class EcgSensorServiceBase:
    is_diagnosis_set = False
    diagnosis_id = 0
    session: Optional[RecordSession]

    __instance = None

    def get_instance(self, db: Session = Depends(get_db)):
        if not EcgSensorServiceBase.__instance:
            EcgSensorServiceBase.__instance = EcgSensorServiceBase(db)
        return EcgSensorServiceBase.__instance

    def __init__(self, db: Session = Depends(get_db)):
        self.__data: Sequence[RecordedData] = []
        self.__db = db
        self.__record_repository = RecordRepository()
        self.__record_session_repository = RecordSessionRepository(self.__db)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.__reading_ecg_sensor_data, "interval", seconds=0.1, jitter=True
        )

    def get_data(self):
        return list(self.__data)

    def start_reading_values(self):
        self.session = self.__record_session_repository.create()
        self.scheduler.start()

    def stop_reading_values(self):
        self.scheduler.pause()

        print(f"Thread status: [{self.scheduler.running}]")

        self.__record_repository.create(self.__data, self.__get_session_id())
        self.__data = []

    def get_sensor_values(self):
        return random.random()

    def __reading_ecg_sensor_data(self):
        if self.is_diagnosis_set and self.session is not None:
            self.is_diagnosis_set = False
            self.__session.DiagnosisId = self.diagnosis_id  # type: ignore
            self.__record_session_repository.save(self.session)
            self.diagnosis_id = 0

        if len(self.__data) >= 1000:
            self.__record_repository.create(self.__data, self.__get_session_id())
            self.__data = []

        current_timestamp = round(time() * 1000)
        list(self.__data).append(
            RecordedData(
                timeStamp=current_timestamp,
                data=self.get_sensor_values(),
            )
        )
        sleep(0.01)

    def __get_session_id(self):
        session_id = 0
        if self.session is not None:
            session_id = self.session.Id
        return session_id
