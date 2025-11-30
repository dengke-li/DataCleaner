from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    def request_validation_exception_handler(request: Request, exc: RequestValidationError):

        # Detect invalid JSON
        json_errors = [
            err for err in exc.errors()
            if err["type"] in ("value_error.jsondecode", "json_invalid")
        ]

        if json_errors:
            # invalid JSON → 400
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": json_errors,
                    "message": "Invalid JSON body"
                },
            )

        # schema/model validation → 422 (FastAPI default)
        print(exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [error['msg'] for error in exc.errors()],
                "message": "Schema Validation error"
            },
        )

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred while processing the request.",
                "message": "Internal server error"
            }
        )