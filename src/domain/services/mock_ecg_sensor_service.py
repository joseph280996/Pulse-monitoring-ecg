import random
import json
import os
from datetime import datetime
from time import sleep
from typing import Sequence
from models.stoppable_thread import StoppableThread
from models.recorded_datum import RecordedData

class EcgSensorService:
    __output_path:str = 'output'
    __instance = None

    def get_instance(self):
        if not EcgSensorService.__instance:
            EcgSensorService.__instance = EcgSensorService()
        return EcgSensorService.__instance

    def __init__(self):
        self.status: bool = False
        self.__data: Sequence[RecordedData] = []
        self.__store_idx: int = 0

    def start_reading_values(self):
        self.__create_dir_if_not_exist()
        self.status = True
        self.__reading_ecg_thread = StoppableThread(
            target=self.__reading_ecg_sensor_data,
            args=(
                self.__data,
                self.status,
                self.__store_idx,
            ),
        )
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.status = False
        if self.__reading_ecg_thread and self.__reading_ecg_thread.is_alive():
            self.__reading_ecg_thread.stop()
        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")
        self.write_data_to_file(self.__data)

    def write_data_to_file(self, data):
        # Serializing json
        model_mapped_data = RecordedData(items=data)
        json_object = model_mapped_data.json()
        with open("build/sample.json", "w") as outfile:
            outfile.write(json_object)

    def __reading_ecg_sensor_data(self, data, status, store_idx):
        while status:
            if len(data[store_idx]) >= 1000:
                self.write_data_to_file(data)
                data.clear()
            current_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            data.append(
                RecordedData(
                    time_stamp=current_timestamp,
                    data=random.random,
                )
            )
            sleep(0.01)

    def __create_dir_if_not_exist(self):
        is_exist = os.path.exists(self.__output_path)
        if not is_exist:
            os.makedirs(self.__output_path)

