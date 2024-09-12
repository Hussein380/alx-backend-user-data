#!/usr/bin/env python3
"""
A module for authentication-related operations, including
user registration,
login validation, session management, and password resetting.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a unique identifier (UUID) for session or token purposes.

    Returns:
        str: A newly generated UUID as a string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to manage authentication processes, including
    user registration, session creation, and password resets.
    """

    def __init__(self):
        """Initializes a new Auth instance and connects to the database."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the database.
        - If the email is already registered, raises a ValueError.
        - Otherwise, hashes the password and creates the user.

        Args:
            email (str): The user's email address.
            password (str): The user's plain text password.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.
        - Checks if the provided email exists and if the password matches
        the stored hash.

        Args:
            email (str): The user's email address.
            password (str): The user's plain text password.

        Returns:
            bool: True if login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a session for the user with the given email by generating
        a session ID.

        Args:
            email (str): The user's email address.

        Returns:
            Union[str, None]: The generated session ID, or None if the user
            is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()  # Generate unique session ID
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves a user by their session ID.

        Args:
            session_id (str): The user's session ID.

        Returns:
            Union[User, None]: The user associated with the session ID,
            or None if not found.
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for the given user by removing their session ID.

        Args:
            user_id (int): The ID of the user whose session is being destroyed.
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for the user with the given email.

        Args:
            email (str): The user's email address.

        Returns:
            str: A password reset token.

        Raises:
            ValueError: If the user with the given email is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")

        reset_token = _generate_uuid()  # Generate unique reset token
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new plain text password.

        Raises:
            ValueError: If the reset token is invalid or not found.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)  # Hash the new password
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
