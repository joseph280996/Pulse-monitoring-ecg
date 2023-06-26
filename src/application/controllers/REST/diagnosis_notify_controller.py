from fastapi import APIRouter, status, Response

from src.application.dtos.diagnosis_notify_dto import DiagnosisNotifyDto
from src.application.handlers.diagnosis_id_notify_handlers import diagnosis_created_notify_handler
from src.domain.factories.sensor_service_factory import SensorServiceFactory


router = APIRouter(
    prefix="/diagnosis",
    tags=["diagnosis"],
    responses={404: {"description": "Not found"}}
)

@router.post("/notify")
async def diagnosis_created_notify(diagnosis_notify_dto: DiagnosisNotifyDto, response: Response):
    diagnosis_created_notify_handler(diagnosis_notify_dto)
    response.status_code = status.HTTP_200_OK
    return {}
