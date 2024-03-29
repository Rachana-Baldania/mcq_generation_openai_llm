"""
    SECURITY FILE
"""
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext

from app.core.configuration import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Generate an access token (JWT) for the specified subject.

    Parameters:
        subject (Union[str, Any]): The subject to be included in the token. It can be a user ID, username, or any unique identifier.
        expires_delta (timedelta, optional): The time duration after which the access token will expire. If not provided, the token will expire after the default duration set in the settings.

    Returns:
        str: The encoded access token as a string.

    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    return _create_token(subject, expire)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Generate a refresh token (JWT) for the specified subject.

    Parameters:
        subject (Union[str, Any]): The subject to be included in the token. It can be a user ID, username, or any unique identifier.
        expires_delta (int, optional): The time duration in minutes after which the refresh token will expire. If not provided, the token will expire after the default duration set in the settings.

    Returns:
        str: The encoded refresh token as a string.
    """

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    return _create_token(subject, expire)


def _create_token(subject: Union[str, Any], expiration_time: int) -> str:
    to_encode = {"exp": expiration_time, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_payload(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    API for Verifying password with the hash value
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    API for Retrieving password hash
    """
    return pwd_context.hash(password)
