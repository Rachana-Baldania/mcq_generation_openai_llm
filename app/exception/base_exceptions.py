"""
    BASE EXCEPTION FILE
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class ModelNotFoundBaseException(HTTPException):
    def __init__(
        self,
        status_code: Optional[int],
        *,
        model_name: str,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        detail = f"{model_name} not found"
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, detail, headers)


class UnAuthorizedBaseException(HTTPException):
    def __init__(
        self,
        *,
        detail: Any = "you are not authorized",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code, detail, headers)


class InternalServerBaseException(HTTPException):
    def __init__(
        self,
        *,
        detail: Any = "there was some issues at server side",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, detail, headers)


class BadRequestBaseException(HTTPException):
    def __init__(
        self, *, detail: Any = "bad request", headers: Optional[Dict[str, Any]] = None
    ) -> None:
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code, detail, headers)


class ConflictBaseException(HTTPException):
    def __init__(
        self,
        *,
        detail: Any = "conflicting request",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code, detail, headers)


incorrect_keyword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Search keyword can't be more than two words!",
    headers={"WWW-Authenticate": "Bearer"},
)


email_not_sent = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Email not sent",
    headers={"WWW-Authenticate": "Bearer"},
)

file_extension_not_supported = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="this file extension is not supported currently",
)

url_type_not_supported = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="this url type is not supported currently",
)
