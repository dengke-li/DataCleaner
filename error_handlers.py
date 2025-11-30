from typing import Any, Optional

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[Any] = None

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        print("error:", exc.errors())

        # Detect invalid JSON
        json_errors = [
            err for err in exc.errors()
            if err["type"] in ("value_error.jsondecode", "json_invalid", "model_attributes_type")
        ]

        if json_errors:
            # invalid JSON → 400
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(error="Invalid JSON body", detail=json_errors).model_dump()
            )

        # schema/model validation → 422 (FastAPI default)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=ErrorResponse(
                error="Schema Validation error",
                detail=[
                    {key: error[key] for key in ['loc', 'msg', 'input']}
                    for error in exc.errors()
                ]
            ).model_dump()
        )

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error="Internal server error",
                detail="An unexpected error occurred while processing the request."
            ).model_dump()
        )