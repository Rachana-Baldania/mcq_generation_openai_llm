from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TimeStampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class JwtTokenSchema(AccessTokenSchema, RefreshTokenSchema):
    token_type: str
