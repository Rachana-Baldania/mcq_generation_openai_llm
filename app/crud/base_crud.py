"""
    BASE CRUD FILE
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import String, cast, or_
from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD CLASS - BASE CRUD
    """

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db_session: Session, id_value: Any) -> Optional[ModelType]:
        """
        Method to retrieve a single object by id
        """
        return db_session.query(self.model).filter(self.model.id == id_value).first()

    def get_multi(
        self, db_session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Method to retrieve multiple objects
        """
        return db_session.query(self.model).offset(skip).limit(limit).all()

    def get_multi_without_limit(self, db_session: Session) -> List[ModelType]:
        """
        Method to retrieve all objects without limit
        """
        return db_session.query(self.model).all()

    def get_multi_fields_filtered(
        self, db_session: Session, only_included_fields: List[str]
    ) -> List[ModelType]:
        """ "
        Method to retrieve only given list of fields names
        """
        query = db_session.query(
            *[getattr(self.model, field) for field in only_included_fields]
        )
        return query.all()

    def search(self, db_session: Session, keyword: str) -> Optional[list[ModelType]]:
        """
        Method to search an object
        """

        return (
            db_session.query(self.model)
            .filter(
                or_(
                    *[
                        cast(self.model.__dict__[column], String).ilike(
                            "%" + keyword + "%"
                        )
                        for column in sa_inspect(self.model).columns.keys()
                        if column in self.model.__searchable__
                    ]
                )
            )
            .all()
        )

    def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Method to Create a new object
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_session: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Method to update an object
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def remove(self, db_session: Session, *, id_value: int) -> ModelType:
        """
        Method to Remove an object
        """
        obj = db_session.query(self.model).get(id_value)
        db_session.delete(obj)
        db_session.commit()
        return obj

    def get_model_data_in_dict(
        self, db_session: Session, only_included_fields: Optional[List[str]] = None
    ) -> List[dict]:
        if only_included_fields:
            queryset = self.get_multi_fields_filtered(
                db_session=db_session, only_included_fields=only_included_fields
            )
        else:
            queryset = self.get_multi_without_limit(db_session=db_session)

        db_row_list = [obj._asdict() for obj in queryset]

        return db_row_list
