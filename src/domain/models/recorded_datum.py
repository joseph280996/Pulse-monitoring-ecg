from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Text
from infrastructure.services.database import Base


class RecordedData(BaseModel):
    time_stamp: str
    data: float


class Record(Base):
    __tablename__ = "Record"

    Id = Column(Integer, primary_key=True, index=True)
    data = Column(Text)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    DiagnosisId = Column(Integer, nullable=True)
    RecordTypeId = Column(Integer, nullable=True)