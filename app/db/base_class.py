"""
    BASE CLASS FILE FOR DB
"""
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all models
    """

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        """
        Method to generate table name automatically in lower case
        """
        return self.__name__.lower()

    @declared_attr
    def __searchable__(self) -> list:
        """
        Method to generate searchable fields automatically
        """
        return []
