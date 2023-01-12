from domain.factories.sensor_service_factory import SensorServiceFactory
from infrastructure.constants.record_operation_types import record_operation_types


def get_record_handler(operation_type_id: int):
    service = SensorServiceFactory.get_instance().get_service()
    if operation_type_id == record_operation_types["START"]:
        return service.get_instance().start_reading_values, "START"

    if operation_type_id == record_operation_types["STOP"]:
        return service.get_instance().stop_reading_values, "STOP"
    raise AttributeError("Unsupported record operation type")
