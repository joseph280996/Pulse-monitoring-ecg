from external_service.query_keys.record_query_key import RecordQueryKeys


class RecordService:
    def __init__(self):
        self.url_path = 'http://localhost:8000'

    async def post(query_keys: RecordQueryKeys):
