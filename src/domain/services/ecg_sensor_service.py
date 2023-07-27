from sqlalchemy.orm import Session
from fastapi import Depends
from time import sleep, time
from typing import Optional
from src.domain.models.record_session import RecordSession
from src.domain.models.stoppable_thread import StoppableThread
from src.domain.models.recorded_datum import RecordedData
from src.domain.services.sensor_service_base import EcgSensorServiceBase
from src.infrastructure.services.database import get_db
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class EcgSensorService(EcgSensorServiceBase):
    diagnosis_id = 0

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db)

    def start_reading_values(self):
        print("Start Reading ecg values")
        self.__create_bus_connection()
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
        )
        self.session = self.__record_session_repository.create()
        self.__reading_ecg_thread.start()

    def get_sensor_value(self):
        return self.chan.value

    def __create_bus_connection(self):
        # Create the I2C busi
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)
        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P1)
