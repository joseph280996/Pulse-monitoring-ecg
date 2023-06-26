from src.domain.factories.sensor_service_factory import SensorServiceFactory
from src.infrastructure.constants.record_operation_types import record_operation_types
from src.infrastructure.services.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_record_handler(operation_type_id: int, db: Session = Depends(get_db), service_factory = SensorServiceFactory()):
    service = service_factory.get_service()
    if operation_type_id == record_operation_types["START"]:
        return service.get_instance(db).start_reading_values

    if operation_type_id == record_operation_types["STOP"]:
        return service.get_instance(db).stop_reading_values
    raise AttributeError("Unsupported record operation type")
