from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Text
from src.infrastructure.services.database import Base


class RecordedData(BaseModel):
    timeStamp: int
    data: float


class Record(Base):
    """The Record entity

    The Record entity that represent a single batch of data storage.

    Attributes:
        Id              Represent the Id of the Record entity
        data            The batch data storage
        dateTimeCreated The UTC timestamp record the creation time of Record entity
        dateTimeUpdated The UTC timestamp record the modification time of Record entity
        RecordSessionId The Foreign Key reference to the RecordSesion entity
    """
    __tablename__ = "Record"

    Id = Column(Integer, primary_key=True, index=True)
    data = Column(Text)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    RecordTypeId = Column(Integer, nullable=False)
