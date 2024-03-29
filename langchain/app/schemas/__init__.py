"""
    INIT FILE FOR SCHEMAS
"""

from .user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    UserBaseSchema,
)
from .response_schema import BaseResponse, FailureResponse
from .email_schema import EmailSchema
