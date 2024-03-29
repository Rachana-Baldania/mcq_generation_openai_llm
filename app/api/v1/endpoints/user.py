"""
    ADMIN ENDPOINTS
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import (
    UserRequestSchema,
    UserResponseSchema,
)

from app.schemas.base_schema import (
    JwtTokenSchema,
    AccessTokenSchema,
    RefreshTokenSchema,
)

from app.crud.user import UserCrud, UserUpdateSchema
from app.api.dependencies import get_user_crud, get_current_user
from app.core.security import (
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_jwt_payload,
)

from app.exception.user_exceptions import (
    user_already_exists,
    user_not_found,
    invalid_jwt_token,
    invalid_credentials,
)

router = APIRouter()


@router.post("/signup", response_model=UserResponseSchema)
def create_user(user: UserRequestSchema, user_crud: UserCrud = Depends(get_user_crud)):
    if user_crud.get_user_by_username(user.username):
        raise user_already_exists

    # hash the password before storing it in database
    user.password = get_password_hash(user.password)
    user = user_crud.create_user(user)
    return user


@router.post("/login")
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_crud: UserCrud = Depends(get_user_crud),
):
    username = form_data.username
    password = form_data.password

    user = user_crud.get_user_by_username(username)

    # if the user does not exists or password is wrong then raise exception
    if user is None or not verify_password(password, user.password):
        raise invalid_credentials

    return JwtTokenSchema(
        token_type="bearer",
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )


@router.post("/refresh_token", response_model=AccessTokenSchema)
def refresh_access_token(
    refresh_token_schema: RefreshTokenSchema,
    user_crud: UserCrud = Depends(get_user_crud),
):
    decoded_refresh_token = decode_jwt_payload(refresh_token_schema.refresh_token)
    username = decoded_refresh_token.get("sub")
    if not username:
        raise invalid_jwt_token

    user = user_crud.get_user_by_username(username)
    if not user:
        raise user_not_found

    return AccessTokenSchema(
        token_type="bearer", access_token=create_access_token(user.username)
    )


@router.patch("/update", response_model=UserResponseSchema)
def update_user(
    user_update: UserUpdateSchema,
    current_user=Depends(get_current_user),
    user_crud: UserCrud = Depends(get_user_crud),
):
    # hash the password before storing it in database
    if user_update.password:
        user_update.password = get_password_hash(user_update.password)

    updated_user = user_crud.update_user(current_user, user_update)
    return updated_user


@router.delete("/delete", response_model=UserResponseSchema)
def delete_user(
    current_user=Depends(get_current_user), user_crud: UserCrud = Depends(get_user_crud)
):
    deleted_user = user_crud.delete_user(current_user)
    return deleted_user


@router.get("/me/", response_model=UserResponseSchema)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
