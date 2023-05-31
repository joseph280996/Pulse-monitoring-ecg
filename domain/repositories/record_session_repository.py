from fastapi import Depends
from domain.models.record_session import RecordSession
from infrastructure.services.database import get_db

class RecordSessionRepository:
    def __init__(self, db = Depends(get_db)):
        self.__db = db

    def create(self):
        record_session = RecordSession(
            RecordTypeId = 2
        )
        return self.save(record_session)
    
    def save(self, record_session: RecordSession):
        self.__db.add(record_session)
        self.__db.commit()
        self.__db.refresh(record_session)
        return record_session
