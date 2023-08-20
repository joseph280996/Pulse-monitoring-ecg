from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from src.infrastructure.services.database import Base

class RecordSession(Base):
    """Represent the RecordSession table

    This is the ORM entity of RecordSession table. It represent
    1 to many relation between Record entities with Diagnosis entity

    Attributes:
        Id              The RecordSessionId
        dateTimeCreated The UTC timestamp of when this entity is created
        dateTimeUpdated The UTC timestamp of when this entity is updated
        DiagnosisId     The Foreign Key reference to the Diagnosis entity
        RecordTypeId    The type of Record
    """
    __tablename__ = "RecordSession"

    Id = Column(Integer, primary_key=True, index=True)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    DiagnosisId = Column(Integer, nullable=True)
    RecordTypeId = Column(Integer, nullable=True)
