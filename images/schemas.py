from ninja import Schema

class UploadResponse(Schema):
    request_id: int
    status: str
    error: str | None = None

class StatusResponse(Schema):
    request_id: int
    status: str
    input_file: str
    output_file: str | None = None