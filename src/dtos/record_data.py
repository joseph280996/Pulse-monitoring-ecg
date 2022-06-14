from pydantic import BaseModel


class RecordData(BaseModel):
    status: str
    recordID: int
