import random
from fastapi import Depends
from sqlalchemy.orm import Session
from time import sleep, time
from typing import Sequence, Optional
from src.domain.models.record_session import RecordSession
from src.domain.models.stoppable_thread import StoppableThread
from src.domain.repositories.record_repository import RecordRepository
from src.domain.repositories.record_session_repository import RecordSessionRepository
from src.infrastructure.services.database import get_db
from models.recorded_datum import RecordedData

class EcgSensorServiceBase:
    is_diagnosis_set = False
    __session: Optional[RecordSession]

    def __init__(self, db: Session = Depends(get_db)):
        self.__data: Sequence[RecordedData] = []
        self.__db = db
        self.__record_repository = RecordRepository()
        self.__record_session_repository = RecordSessionRepository(self.__db)

    def start_reading_values(self):
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
        )
        self.__session = self.__record_session_repository.create()
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.__reading_ecg_thread.stop()

        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")

        self.__record_repository.create(self.__data, self.__get_session_id())
        self.__data = []

    def __reading_ecg_sensor_data(self, stop_event):
        while not stop_event.is_set():
            if self.is_diagnosis_set and self.__session is not None:
                self.is_diagnosis_set = False
                self.__session.DiagnosisId = self.__diagnosis_id # type: ignore
                self.__diagnosis_id = 0
                self.__record_session_repository.save(self.__session)

            if len(self.__data) >= 1000:
                self.__record_repository.create(self.__data, self.__get_session_id())
                self.__data = []

            current_timestamp = round(time() * 1000)
            list(self.__data).append(
                RecordedData(
                    timeStamp=current_timestamp,
                    data=random.random(),
                )
            )
            sleep(0.01)
    def __get_session_id(self):
        session_id = 0
        if self.__session is not None:
            session_id = self.__session.Id
        return session_id

