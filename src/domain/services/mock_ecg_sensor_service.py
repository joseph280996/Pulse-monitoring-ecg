from fastapi import Depends
from sqlalchemy.orm import Session
from src.domain.services.sensor_service_base import EcgSensorServiceBase
from src.infrastructure.services.database import get_db

class MockEcgSensorService(EcgSensorServiceBase):
    is_diagnosis_set = False
    diagnosis_id = 0
    __instance = None

    def get_instance(self):
        if not MockEcgSensorService.__instance:
            MockEcgSensorService.__instance = MockEcgSensorService()
        return MockEcgSensorService.__instance

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db)

