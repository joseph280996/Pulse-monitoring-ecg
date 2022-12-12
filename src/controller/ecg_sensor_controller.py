import json
from typing import Sequence
from src.dependencies.reading_ecg_sensor_data import reading_ecg_sensor_data
from src.dependencies.stoppable_thread import StoppableThread
from src.models.recorded_datum import RecordedDatum, RecordedData
import json


class _EcgSensorController:
    def __init__(self):
        self.status: bool = False
        self.__data: Sequence[Sequence[RecordedDatum]] = [[]]
        self.__store_idx: int = 0

    def start_reading_values(self):
        self.status = True
        self.__reading_ecg_thread = StoppableThread(
            target=reading_ecg_sensor_data, args=(self.__data, self.status, self.__store_idx,))
        self.__reading_ecg_thread.start()

    def stop_reading_values(self):
        self.status = False
        if self.__reading_ecg_thread and self.__reading_ecg_thread.is_alive():
            self.__reading_ecg_thread.stop()
        print(f"Thread status: [{self.__reading_ecg_thread.stopped()}]")
        self.write_data_to_file()

    def get_data(self):
        return self.__data

    def write_data_to_file(self):
        # Serializing json
        model_mapped_data = RecordedData(items=self.__data)
        json_object = model_mapped_data.json()
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)


ecg_sensor_controller = _EcgSensorController()
