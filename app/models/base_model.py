from datetime import datetime
from sqlalchemy.types import DateTime
from sqlalchemy import Column

from app.db.base_class import Base


class TimeStampModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)
