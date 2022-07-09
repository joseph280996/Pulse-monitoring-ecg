from src.controller.ecg_sensor_controller import ecg_sensor_controller
from src.variables.record_operation_types import record_operation_types


def get_record_handler(operation_type_id: int):
    print(record_operation_types["START"])
    if operation_type_id == record_operation_types["START"]:
        return ecg_sensor_controller.start_reading_values, "START"

    print(record_operation_types["STOP"])
    if operation_type_id == record_operation_types["STOP"]:
        return ecg_sensor_controller.stop_reading_values, "STOP"
    raise AttributeError("Unsupported record operation type")
