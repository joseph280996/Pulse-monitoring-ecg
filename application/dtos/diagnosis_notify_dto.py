from pydantic import BaseModel


class DiagnosisNotifyDto(BaseModel):
    diagnosisId: int