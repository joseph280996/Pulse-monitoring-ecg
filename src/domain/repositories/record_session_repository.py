from fastapi import Depends
from src.domain.models.record_session import RecordSession
from src.infrastructure.services.database import get_db

class RecordSessionRepository:
    def __init__(self, db = Depends(get_db)):
        self.__db = db

    def create(self, diagnosisId):
        record_session = RecordSession(
            RecordTypeId = 2,
            diagnosisId = diagnosisId
        )
        self.__db.add(record_session)
        self.__db.commit()
        self.__db.refresh(record_session)
        return record_session
