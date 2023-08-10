import random
import importlib
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends
from sqlalchemy.orm import Session
from time import time
from typing import List, Optional
from src.domain.data_accessors.sensor_data_accessor import SensorDataAccessor
from src.domain.models.record_session import RecordSession
from src.domain.repositories.record_repository import RecordRepository
from src.domain.repositories.record_session_repository import RecordSessionRepository
from src.infrastructure.services.database import get_db
from models.recorded_datum import RecordedData


class EcgSensorManager:
    """The base class of ECG sensor service.

    This is the base class of ECG sensor service which has all the main
    functionality that is shared between the local development mock service
    with the actual service. Due to multiple packages that can't be built
    when ran on development computer, through dynamic importing, we're
    bypassing that with mock service to fully test the functionality.

    Attributes:
        is_diagnosis_set(bool): A boolean that indicated whether the diagnosis_id was set
        diagnosis_id(bool): The Diagnosis Id that was created in Piezo sensor service.
        session(Session): The session that was created when running the scheduler.
    """

    __session: RecordSession
    __instance = None
    __scheduler: AsyncIOScheduler
    __data_accessor: Optional[SensorDataAccessor] = None

    @property
    def session(self) -> RecordSession:
        """The current record session"""
        return self.__session

    @session.setter
    def set_session(self, session: RecordSession):
        self.__session = session

    @property
    def scheduler(self) -> AsyncIOScheduler:
        """A Scheduler to run function in interval"""
        return self.__scheduler

    @staticmethod
    def get_instance(db: Session = Depends(get_db)):
        """Get the current instance of EcgSensorService

        Retrieve or create a new instance of EcgSensorServiceBase for singleton
        implementation.

        Returns:
            The instance of EcgSensorServiceBase and maintain singleton design.
        """

        if not EcgSensorManager.__instance:
            EcgSensorManager.__instance = EcgSensorManager(db=db)
        return EcgSensorManager.__instance

    def __init__(
        self, db: Session = Depends(get_db)
    ):
        if EcgSensorManager.__instance is not None:
            raise Exception("Failed to create a new instance because this is a singleton class, please use get_instance instead.")

        self.__data: List[RecordedData] = []
        self.__secondary_data: List[RecordedData] = []
        self.__db = db

        self.__record_repository = RecordRepository()
        self.__record_session_repository = RecordSessionRepository(self.__db)

        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.add_job(
            self.__reading_ecg_sensor_data, "interval", seconds=0.1, jitter=True
        )

        """Because directly import in development environment will cause an issue, we'll use dynamic import
        so if the condition is not met, python will not try to import packages that are failed to installed
        in development environment
        """
        if os.getenv("RUNNING_ENV") != "development":
            self.__data_accessor = importlib.import_module("src.domain.data_accessors.sensor_data_accessor").SensorDataAccessor()

    def get_data(self) -> List[RecordedData]:
        """Get the current data in buffer

        Retrieve the current amount of data in the buffer to send back
        to front end for real-time display. If current buffer doesn't have
        enough data points, this will check and append the secondary store
        to make up for it.

        Returns:
            A list of data that will be sent to the front end for display
            with the following format:
            [
                {
                    timestamp: UTC timestamp string,
                    data: sensor data float
                }
            ]
        """

        if len(self.__data) < 20:
            return (self.__data + self.__secondary_data)[-20:]
        return list(self.__data)

    def start_reading_values(self) -> None:
        """Start reading sensor values cycle.

        Create a new session and start up the scheduler to read sensor values
        in interval.
        """

        self.set_session(self.__record_session_repository.create())
        self.scheduler.start()

    def stop_reading_values(self, diagnosis_id: int) -> None:
        """Stop the reading sensor values cycle.

        Pause the scheduler so that we can start later on, save the recorded data into the database,
        and update RecordSession with the provided DiagnosisId from the front end
        
        Reset the current read buffer.
        """
        if self.__session is None:
            raise Exception("Stopping reading sensor value with starting detected.")

        self.scheduler.pause()

        print(f"Scheduler Paused with status: [{self.scheduler.running}]")

        self.__record_repository.create(self.__data, self.__session.Id)

        self.__session.DiagnosisId = diagnosis_id  #type: ignore
        self.__record_session_repository.save(self.__session)

        self.__reset_storage()


    def get_sensor_values(self) -> float:
        """Get the mock sensor value.

        Retrieve the mock sensor value generated by random.
        This function will be override to get sensor value through GPIO
        when run on Raspberry PI environment.

        Returns:
            A float value of the sensor value or a random float value for testing purposes.
        """
        if self.__data_accessor is not None:
            return self.__data_accessor.get_sensor_data()

        return random.random()

    def __reading_ecg_sensor_data(self):
        if len(self.__data) >= 1000:
            temp = self.__data
            self.__data = self.__secondary_data
            self.__secondary_data = temp
            self.__record_repository.create(self.__secondary_data, self.__session.Id)

        current_timestamp = round(time() * 1000)
        list(self.__data).append(
            RecordedData(
                timeStamp=current_timestamp,
                data=self.get_sensor_values(),
            )
        )
    def __reset_storage(self):
        self.__data = []
        self.__secondary_data = []
