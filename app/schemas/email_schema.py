"""
    EMAIL SCHEMA
"""

from typing import List
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    """
    Email Schema
    """

    email: List[EmailStr]
