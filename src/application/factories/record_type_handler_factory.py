from domain.service.ecg_sensor_service import EcgSensorService
from infrastructure.variables.record_operation_types import record_operation_types


def get_record_handler(operation_type_id: int):
    print(record_operation_types["START"])
    if operation_type_id == record_operation_types["START"]:
        return EcgSensorService.get_instance().start_reading_values, "START"

    print(record_operation_types["STOP"])
    if operation_type_id == record_operation_types["STOP"]:
        return EcgSensorService.get_instance().stop_reading_values, "STOP"
    raise AttributeError("Unsupported record operation type")
