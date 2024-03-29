"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    user,
    test,
    document_search,
    file_upload,
    url_upload,
    chat,
    stream_demo,
)

api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
api_router.include_router(document_search.router, tags=["Document-search"])
api_router.include_router(file_upload.router, tags=["File-upload"])
api_router.include_router(url_upload.router, tags=["Url-upload"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(stream_demo.router, tags=["stream"])
