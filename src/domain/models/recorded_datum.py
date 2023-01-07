from pydantic import BaseModel
from typing import List


class RecordedDatum(BaseModel):
    time_stamp: str
    data: float

class RecordedData(BaseModel):
    items: List[List[RecordedDatum]]