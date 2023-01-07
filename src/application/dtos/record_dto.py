from pydantic import BaseModel

class RecordDto(BaseModel):
    status: int
    operation_type_id: int
