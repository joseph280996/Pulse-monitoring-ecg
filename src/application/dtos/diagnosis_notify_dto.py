from pydantic import BaseModel


class DiagnosisNotifyDto(BaseModel):
    """The Diagnosis Notify POST body

    The Diagnosis Notify POST body representation

    Attributes:
        diagnosisId     The new DiagnosisId created by Piezoelectric sensor
    """
    diagnosisId: int
