"""
    TEST ENDPOINTS
"""
from typing import Any

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from app.worker import test_celery


router = APIRouter()


@router.get("/celery")
async def test():
    task = test_celery.delay(word="hello world")
    return JSONResponse({"task_id": task.id})
