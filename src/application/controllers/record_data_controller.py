from fastapi import APIRouter, Response, status
from application.factories.record_type_handler_factory import get_record_handler
from application.dtos.record_dto import RecordDto

router = APIRouter()


@router.post("/record")
async def recording(record_dto: RecordDto, response: Response):
    try:
        handler, response_status = get_record_handler(
            record_dto.operation_type_id
        )
        handler()

        response.status_code = status.HTTP_202_ACCEPTED
        return {"status": response_status}
    except AttributeError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Invalid argument [operation_type_id]"}
