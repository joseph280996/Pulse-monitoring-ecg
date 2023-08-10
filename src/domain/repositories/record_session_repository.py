from fastapi import Depends
from src.domain.models.record_session import RecordSession
from src.infrastructure.services.database import get_db


class RecordSessionRepository:
    """Record Session Repository

    This class handles all interactions with the database data.
    """
    def __init__(self, db=Depends(get_db)):
        self.__db = db

    def create(self) -> RecordSession:
        """Create record Session

        Create a new record session in the database.

        Returns:
            A new pydantic RecordSession object.
        """
        record_session = RecordSession(RecordTypeId=2)
        return self.save(record_session)

    def save(self, record_session: RecordSession):
        """Save any update to a given RecordSession

        Update all information of an existing record session

        Returns:
            An updated pydantic RecordSession object.
        """
        self.__db.add(record_session)
        self.__db.commit()
        self.__db.refresh(record_session)
        return record_session

    def assign_diagnosis_id(self, diagnosis_id: int):
        """Assign DiagnosisId to all ECG Record type

        Update DiagnosisId of all existing ECG Record type that isn't attached to
        any Diagnosis.

        Returns:
            A boolean that indicate the update was executed successfully
        """
        query = "UPDATE RecordSession SET DiagnosisId = :diagnosis_id WHERE RecordTypeId = :record_type_id AND DiagnosisId IS NULL;"
        self.__db.execute(query, {"diagnosis_id": diagnosis_id, "record_type_id": 2})
        return True
