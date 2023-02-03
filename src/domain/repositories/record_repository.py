from domain.models.recorded_datum import RecordedData
from infrastructure.services.file_system_service import FileSystemService


class RecordRepository:
    __instance = None
    __output_path = "output/"
    __previous_file_id = 0
    __file_id = 0

    def get_instance():
        if not RecordRepository.__instance:
            RecordRepository.__instance = RecordRepository()

        return RecordRepository.__instance

    def set_previous_file_id():
        RecordRepository.__previous_file_id = RecordRepository.__file_id

    def __init__(self):
        self.file_system_service = FileSystemService()

    def create(self, data):
        model_mapped_data = RecordedData(items=data)
        path = "{0}record{1}.json".format(
            self.__output_path, RecordRepository.__file_id
        )

        self.file_system_service.write_data_to_file(model_mapped_data, path)
        RecordRepository.__file_id += 1

    def get_all_records(self):
        result_data = list()
        for file_id in range(
            RecordRepository.__previous_file_id, RecordRepository.__file_id
        ):
            path = "{0}record{1}.json".format(self.__output_path, file_id)
            data = self.file_system_service.read_data_from_file(path)
            result_data = result_data + data["items"]

        return result_data
