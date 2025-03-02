from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.app_logging import logger

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    logger.exception("Request validation error")
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
