from pydantic import BaseModel


class RecordedDatum(BaseModel):
    time_stamp: str
    data: float
