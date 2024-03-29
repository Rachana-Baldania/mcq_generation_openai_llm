"""
    MAIN APP FILE
"""
import aioredis
import logging
import uvicorn
import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.core.configuration import settings

logger = logging.getLogger(__name__)


# if settings.SENTRY_DSN:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         traces_sample_rate=1.0,
#     )
# else:
#     logger.warning("Sentry DSN not set")

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTPException
    """
    try:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
            },
        )
    except Exception as excep:
        return JSONResponse(
            status_code=500,
            content={
                "message": str(excep),
            },
        )


@app.on_event("startup")
async def startup():
    """
    Connect to Redis on startup
    """
    try:
        redis = await aioredis.Redis.from_url(settings.REDIS_HOST_URL)
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error("Error connecting to Redis, %s", e)
        return JSONResponse(
            status_code=500,
            content={
                "message": str(e),
            },
        )


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# TODO: to start the application in below mentioned way
# if __name__ == "__main__":
#     uvicorn.run(
#         app=app,
#         host=settings.HOST,
#         port=settings.PORT,
#         reload=settings.RELOAD,
#         factory=True,
#     )
