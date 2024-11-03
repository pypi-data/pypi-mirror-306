from fastapi import FastAPI, Request, HTTPException

from .resources import entity
from .errors.app import DtoValidationException, PermissionDeniedException


__all__ = ["setup", "entity"]


def setup(app: FastAPI):
    @app.exception_handler(DtoValidationException)
    async def validation_exception_handler(
        request: Request, exc: DtoValidationException
    ):
        raise HTTPException(status_code=400, detail=exc.dto_errors)

    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_exception_handler(
        request: Request, exc: PermissionDeniedException
    ):
        raise HTTPException(status_code=403, detail=str(exc))
