from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text
from src.infrastructure.services.database import Base

class RecordSession(Base):
    __tablename__ = "RecordSession"

    Id = Column(Integer, primary_key=True, index=True)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    DiagnosisId = Column(Integer, nullable=True)
    RecordTypeId = Column(Integer, nullable=True)