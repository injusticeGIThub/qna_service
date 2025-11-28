from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.core.exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    details = jsonable_encoder(exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "code": "validation_error",
            "details": details,
        },
    )
