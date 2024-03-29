"""
    USER SCHEMA FILE
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, UUID4

from app.schemas.base_schema import TimeStampSchema


class UserBaseSchema(BaseModel):
    """
    User Base Schema
    """

    username: str
    email: EmailStr


class UserRequestSchema(UserBaseSchema):
    password: str


# Properties to receive via API on creation
class UserCreateSchema(UserRequestSchema):
    """
    User Create Schema
    """

    pass


# Properties to receive via API on update
class UserUpdateSchema(UserBaseSchema):
    """
    User Update Schema
    """

    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


# schema for sending user properties via API
class UserResponseSchema(UserBaseSchema, TimeStampSchema):
    id: UUID4

    class Config:
        orm_mode = True


class UserListResponseSchema(BaseModel):
    users: List[UserResponseSchema]
