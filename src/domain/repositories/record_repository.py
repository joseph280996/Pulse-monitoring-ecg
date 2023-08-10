import json
from fastapi import Depends
from src.domain.models.recorded_datum import Record
from src.infrastructure.services.database import get_db


class RecordRepository:
    """Record Repository

    A repository that handles any update or creation of Record object in database
    """

    def __init__(self, db = Depends(get_db)):
        self.__db = db

    def create(self, data, record_session_id):
        """Create Record

        Convert the received data to a JSON string and creating a new Record in the database

        Returns:
            A new pydantic Record object
        """
        stringified_data = json.dumps([item.dict() for item in data])
        record = Record(
            data=stringified_data,
            RecordSessionId= record_session_id
        )
        self.__db.add(record)
        self.__db.commit()
        self.__db.refresh(record)
