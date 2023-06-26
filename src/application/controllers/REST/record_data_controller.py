from fastapi import APIRouter, Response, status, Depends
from src.application.factories.record_type_handler_factory import get_record_handler
from src.domain.repositories.record_repository import RecordRepository
from src.application.dtos.record_dto import RecordDto

router = APIRouter(
    prefix="/record", tags=["record"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def recording(record_dto: RecordDto, response: Response):
    try:
        handler = get_record_handler(record_dto.operation_type_id)
        handler()

        response.status_code = status.HTTP_202_ACCEPTED
        return {"status": record_dto.operation_type_id}
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_]"}


@router.get("/")
async def get_records(response: Response):
    try:
        raise NotImplemented()
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_id]"}
