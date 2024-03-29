"""
    RESPONSE SCHEMA FILE
"""
from typing import Union, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    """
    Base Response Schema
    """

    success: bool
    message: str
    data: Optional[Union[dict, list]]


class FailureResponse(BaseResponse):
    """
    Failure Response Schema
    """

    errorCode: Optional[int]
