from fastapi import APIRouter, Response, status, Depends
from src.domain.repositories.record_repository import RecordRepository
from src.application.dtos.record_dto import RecordDto

router = APIRouter(
    prefix="/record", tags=["record"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def recording(record_dto: RecordDto, response: Response):
    try:

        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "Deprecated endpoint"}
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_]"}


@router.get("/")
async def get_records(response: Response):
    try:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "This features is under development!"}
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_id]"}
