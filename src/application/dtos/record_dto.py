from pydantic import BaseModel

class RecordDto(BaseModel):
    operation_type_id: int
