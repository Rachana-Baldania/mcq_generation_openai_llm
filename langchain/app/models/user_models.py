"""
    USER MODEL FILE
"""
import uuid, re

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship, validates

from app.models.base_model import TimeStampModel


class User(TimeStampModel):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    # Regular expression pattern for email validation
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(self.email_regex, email):
            raise ValueError("Invalid email address format")
        return email

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}')>"
