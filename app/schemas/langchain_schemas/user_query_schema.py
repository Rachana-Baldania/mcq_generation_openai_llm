from pydantic import BaseModel, Field


class UserQuerySchema(BaseModel):
    user_query: str = Field(..., max_length=400)
