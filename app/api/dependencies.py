"""
    DEPENDENCIES FILE FOR ROUTES
"""
from typing import Generator, Optional, List, Dict
from uuid import UUID
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from langchain.vectorstores import VectorStore

from app import models
from app.crud import user
from app.core import security
from app.core.configuration import settings
from app.db.session import SessionLocal

from app.exception.vectordb_exceptions import vector_index_not_created,vectordb_does_not_exists,vectordb_not_connected
from app.exception.user_exceptions import invalid_credentials,user_not_found,expired_jwt_token,invalid_jwt_token

from vectorstore.vector_db_mappings import VECTOR_DB_MAPPING

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="current page number"),
        page_size: int = Query(
            default=10, ge=1, le=100, description="number of items per page"
        ),
    ) -> None:
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


# defaults to pinecone but you can use different vector db for different request
def get_vector_db(vectordb_name: str = "pinecone") -> Optional[VectorStore]:
    """
    Get the vector database object based on the specified database name.

    Args:
        vectordb_name (str, optional): The name of the vector database to retrieve.
            Default is 'pinecone'.

    Returns:
        VectorStore: An instance of the vector database object corresponding to the specified database name.

    Raises:
        HTTPException: If the specified database name is not supported or if there is an internal server error.

    Note:
        This function relies on the global dictionary VECTOR_DB_MAPPING to map database names to vector database objects.
        If the provided vectordb_name is not found in the mapping, a ValueError is raised.
    """
    try:
        vector_db = VECTOR_DB_MAPPING.get(vectordb_name)
        if vector_db:
            return vector_db

    except ValueError as ve:
        raise vectordb_does_not_exists from ve
    except Exception as exc:
        raise vectordb_not_connected from exc


def get_db() -> Generator:
    """
    Returns a new database session
    """
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        db_session.close()


def get_user_crud(db: Session = Depends(get_db)) -> user.UserCrud:
    return user.UserCrud(db)


def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_crud: user.UserCrud = Depends(get_user_crud),
) -> user.User:
    try:
        payload = security.decode_jwt_payload(token)
        token_data = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise expired_jwt_token

    except jwt.InvalidTokenError:
        raise invalid_jwt_token

    except (jwt.JWTError, ValidationError) as excep:
        raise invalid_credentials from excep

    user = user_crud.get_user_by_username(token_data)

    if not user:
        raise user_not_found

    return user


def get_current_active_user(
    current_user: user.User = Depends(get_current_user),
    user_crud: user.UserCrud = Depends(get_user_crud),
) -> user.User:
    """
    Return the current active user
    """
    if not user_crud.is_active(current_user):
        raise UnAuthorizedBaseException(detail="Inactive user")

    return current_user


def get_current_active_superuser(
    current_user: user.User = Depends(get_current_user),
    user_crud: user.UserCrud = Depends(get_user_crud),
) -> user.User:
    """
    Return the current active superuser
    """
    if not user_crud.is_superuser(current_user):
        raise UnAuthorizedBaseException(detail="not a superuser")

    return current_user
