import json
from typing import Sequence
from src.dependencies.reading_ecg_sensor_data import reading_ecg_sensor_data
from src.dependencies.stoppable_thread import StoppableThread

from src.models.recorded_datum import RecordedDatum


class EcgSensorController:
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
        print(self.__data)
        print(self.__reading_ecg_thread.stopped())

    def write_data_to_file(self):
        # Serializing jso
        json_object = json.dumps(self.__data, indent=4)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
