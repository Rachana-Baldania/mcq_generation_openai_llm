from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user_models import User
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema


class UserCrud:
    """
    CRUD operations for managing User data.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the UserCrud with a database session.

        Args:
        - db (Session): The SQLAlchemy database session.
        """
        self.db = db

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
        - user_id (str): The ID of the user to retrieve.

        Returns:
        - Optional[User]: The User object if found, or None if the user doesn't exist.

        """
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        Args:
        - email (str): The email of the user to retrieve.

        Returns:
        - Optional[User]: The User object if found, or None if the user with the email doesn't exist.
        """

        user = self.db.query(User).filter(User.email == email).first()
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        Args:
        - username (str): The username of the user to retrieve.

        Returns:
        - Optional[User]: The User object if found, or None if the user with the user doesn't exist.
        """

        user = self.db.query(User).filter(User.username == username).first()
        return user

    def create_user(self, user: UserCreateSchema) -> User:
        """
        Create a new user.

        Args:
        - user (UserCreateSchema): The user data to create a new user.

        Returns:
        - User: The created User object.

        """
        user_model = User(**user.dict())
        self.db.add(user_model)

        self.db.commit()
        return user_model

    def update_user(self, user_model: User, user: UserUpdateSchema) -> User:
        """
        Update an existing user by their ID.

        Args:
        - user_id (str): The ID of the user to update.
        - user (UserUpdateSchema): The updated user data.

        Returns:
        - User: The updated User object.

        """

        for attr, value in user.dict(exclude_unset=True).items():
            setattr(user_model, attr, value)

        self.db.commit()
        self.db.refresh(user_model)
        return user_model

    def delete_user(self, user_model: User) -> User:
        """
        Delete a user by their ID.

        Args:
        - user_id (str): The ID of the user to delete.

        Returns:
        - User: The deleted User object.

        """

        self.db.delete(user_model)
        self.db.commit()
        user_model.deleted_at = datetime.utcnow()
        return user_model
