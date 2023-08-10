from fastapi import APIRouter, status, Response

from src.application.dtos.diagnosis_notify_dto import DiagnosisNotifyDto
from src.application.handlers.diagnosis_id_notify_handlers import diagnosis_created_notify_handler


router = APIRouter(
    prefix="/diagnosis",
    tags=["diagnosis"],
    responses={404: {"description": "Not found"}}
)

@router.post("/notify")
async def diagnosis_created_notify(diagnosis_notify_dto: DiagnosisNotifyDto, response: Response):
    """Diagnosis created notify controller

    This function will cascade the received request down to appropriate handler
    and have top level try catch block to update status code accordingly
    """
    try:
        diagnosis_created_notify_handler(diagnosis_notify_dto)
        response.status_code = status.HTTP_200_OK
    except:
        print("Error updating diagnosis id")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return {}

