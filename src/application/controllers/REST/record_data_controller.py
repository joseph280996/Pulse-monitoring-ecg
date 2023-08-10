from fastapi import APIRouter, Response, status

"""
Legacy code, keep to determine whether to delete or keep
"""

router = APIRouter(
    prefix="/record", tags=["record"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def recording(response: Response):
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
