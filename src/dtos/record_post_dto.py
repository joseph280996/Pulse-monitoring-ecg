from pydantic import BaseModel


class RecordPostDto(BaseModel):
    sessionID: int
