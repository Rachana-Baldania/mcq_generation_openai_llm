from fastapi import status
from .base_exceptions import (
    ModelNotFoundBaseException,
    UnAuthorizedBaseException,
    BadRequestBaseException,
    ConflictBaseException,
)

user_not_found = ModelNotFoundBaseException(
    model_name="user",
    status_code= status.HTTP_404_NOT_FOUND,
    detail="User Does Not Exist! Please Register First.",
    headers={"WWW-Authenticate": "Bearer"},
)

user_already_exists = ConflictBaseException(
    detail="User already exists.",
    headers={"WWW-Authenticate": "Bearer"},
)


email_already_exists = ConflictBaseException(
    detail="User with this email already exists!",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_password = UnAuthorizedBaseException(
    detail="Invalid password!",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_credentials = UnAuthorizedBaseException(
    detail="Invalid credentials!",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_jwt_token = UnAuthorizedBaseException(detail="provided token is invalid")

expired_jwt_token = UnAuthorizedBaseException(detail="provided token has expired")
