from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, error: str, code: str, status_code: int):
        super().__init__(
            status_code=status_code,
            detail={"error": error, "code": code},
        )


class NotFound(AppException):
    def __init__(self, error="Resource not found", code="not_found"):
        super().__init__(
            error=error,
            code=code,
            status_code=status.HTTP_404_NOT_FOUND
        )


class BadRequest(AppException):
    def __init__(self, error="Bad request", code="bad_request"):
        super().__init__(
            error=error,
            code=code,
            status_code=status.HTTP_400_BAD_REQUEST
        )
