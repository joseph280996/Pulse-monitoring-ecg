import json
import os
from datetime import datetime
from time import sleep
from typing import Sequence
from domain.models.stoppable_thread import StoppableThread
from domain.models.recorded_datum import RecordedDatum, RecordedData
from domain.repositories.record_repository import RecordRepository
from infrastructure.services.file_system_service import FileSystemService
import json
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class EcgSensorService:
    __output_path: str = "output/"
    __instance = None

    def get_instance():
        if not EcgSensorService.__instance:
            EcgSensorService.__instance = EcgSensorService()
        return EcgSensorService.__instance

    def __init__(self):
        self.status: bool = False
        self.__data: Sequence[RecordedDatum] = []
        self.__record_repository = RecordRepository.get_instance()

    def start_reading_values(self):
        print("Start Reading ecg values")
        self.__create_dir_if_not_exist()
        self.status = True
        self.__create_bus_connection()
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
            args=(
                self.__data,
                self.status,
            ),
        )
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.status = False
        if self.__reading_ecg_thread and self.__reading_ecg_thread.is_alive():
            self.__reading_ecg_thread.stop()

        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")

        self.__record_repository.create(self.__data)
        RecordRepository.set_previous_file_id()

    def __reading_ecg_sensor_data(self, data, status):
        while status:
            if len(data) >= 1000:
                print("Start Saving collected data")
                self.__record_repository.create(self.__data)
                data.clear()
            current_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            data.append(
                RecordedDatum(
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

    def __create_dir_if_not_exist(self):
        is_exist = os.path.exists(self.__output_path)
        if not is_exist:
            os.makedirs(self.__output_path)
