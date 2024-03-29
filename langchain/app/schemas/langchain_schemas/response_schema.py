from typing import List
from pydantic import BaseModel


class DocumentSchema(BaseModel):
    page_content: str
    source: str


class FinalResponseSchema(BaseModel):
    success: bool
    message: str
    answer: str
    sources: List[DocumentSchema]
