
from fastapi import APIRouter, Depends, status, Response

from src.application.dtos.diagnosis_notify_dto import DiagnosisNotifyDto
from src.domain.factories.sensor_service_factory import SensorServiceFactory
from src.infrastructure.services.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/diagnosis",
    tags=["diagnosis"],
    responses={404: {"description": "Not found"}}
)

@router.post("/notify")
async def diagnosisCreatedNotify(diagnosis_notify_dto: DiagnosisNotifyDto, response: Response, db: Session = Depends(get_db)):
    service = SensorServiceFactory.get_instance().get_service()
    service_instance = service.get_instance(db)
    service_instance.__diagnosis_id = diagnosis_notify_dto.diagnosisId
    response.status_code = status.HTTP_200_OK
    return {}
