from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime
from time import sleep
from typing import Sequence
from domain.models.stoppable_thread import StoppableThread
from domain.models.recorded_datum import RecordedData
from domain.repositories.record_repository import RecordRepository
from infrastructure.services.database import get_db
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from src.domain.repositories.record_session_repository import RecordSessionRepository


class EcgSensorService:
    __instance = None
    __diagnosis_id = 0
    __session_id = 0

    def set_diagnosis_id(self, diagnosisId):
        self.__diagnosis_id =  diagnosisId

    def get_instance(db: Session = Depends(get_db)):
        if not EcgSensorService.__instance:
            EcgSensorService.__instance = EcgSensorService(db)
        return EcgSensorService.__instance

    def __init__(self, db:Session = Depends(get_db)):
        self.__data: Sequence[RecordedData] = []
        self.__db = db
        self.__record_repository = RecordRepository(self.__db)
        self.__record_session_repository = RecordSessionRepository(self.__db)

    def start_reading_values(self):
        print("Start Reading ecg values")
        self.__create_bus_connection()
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
        )
        new_session = self.__record_session_repository.create(self.__diagnosis_id)
        self.__session_id = new_session.Id
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.__reading_ecg_thread.stop()

        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")

        self.__record_repository.create(self.__data, )
        self.__data.clear()

    def __reading_ecg_sensor_data(self, stop_event):
        while not stop_event.is_set():
            if len(self.__data) >= 1000:
                self.__record_repository.create(self.__data, self.__diagnosis_id, self.__session_id)
                self.__data.clear()
            current_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            self.__data.append(
                RecordedData(
                    time_stamp=current_timestamp,
                    data=self.chan.value,
                )
            )
            sleep(0.01)

    def __create_bus_connection(self):
        # Create the I2C busi
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)
        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P1)
