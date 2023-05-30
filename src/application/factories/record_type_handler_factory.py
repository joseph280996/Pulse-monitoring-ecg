from domain.factories.sensor_service_factory import SensorServiceFactory
from infrastructure.constants.record_operation_types import record_operation_types
from sqlalchemy.orm import Session
from fastapi import Depends
from infrastructure.services.database import get_db

def get_record_handler(operation_type_id: int, db:Session = Depends(get_db)):
    service = SensorServiceFactory.get_instance().get_service()
    if operation_type_id == record_operation_types["START"]:
        return service.get_instance(db).start_reading_values, "START"

    if operation_type_id == record_operation_types["STOP"]:
        return service.get_instance(db).stop_reading_values, "STOP"
    raise AttributeError("Unsupported record operation type")
