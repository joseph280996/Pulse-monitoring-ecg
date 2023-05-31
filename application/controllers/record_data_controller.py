from fastapi import APIRouter, Response, status, Depends
from application.factories.record_type_handler_factory import get_record_handler
from domain.repositories.record_repository import RecordRepository
from application.dtos.record_dto import RecordDto
from sqlalchemy.orm import Session

from infrastructure.services.database import get_db

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def recording(record_dto: RecordDto, response: Response, db: Session = Depends(get_db)):
    try:
        handler, response_status = get_record_handler(record_dto.operation_type_id, db)
        handler()

        response.status_code = status.HTTP_202_ACCEPTED
        return {"status": response_status}
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_]"}


@router.get("/")
async def get_records(response: Response):
    try:
        record_repository = RecordRepository.get_instance()
        records = record_repository.get_all_records()

        response.status_code = status.HTTP_202_ACCEPTED
        return records
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_id]"}
