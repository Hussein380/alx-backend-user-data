#!/usr/bin/env python3
"""DB module for managing the application's database interactions.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """
    DB class to handle database operations for the application, including
    adding new users, finding users, and updating user records.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the DB class.
        - Creates the SQLite engine and sets up the database schema.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # Drops all tables (for development purposes)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)  # Creates all tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoizes and returns the session object for database transactions.

        Returns:
            Session: The current session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed version of the user's password.

        Returns:
            User: The newly created user object.

        Raises:
            Exception: If the user cannot be added to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except Exception:
            self._session.rollback()  # Roll back in case of error
            return None

    def find_user_by(self, **filters) -> User:
        """
        Finds a user in the database using specific filter criteria.

        Args:
            **filters: Keyword arguments specifying the attributes to filter.

        Returns:
            User: The user object that matches the filters.

        Raises:
            InvalidRequestError: If the filter key is not a valid User att
            NoResultFound: If no user is found matching the filters.
        """
        # Validate the filter keys against the User model
        columns, values = [], []
        for key, value in filters.items():
            if hasattr(User, key):
                columns.append(getattr(User, key))  # Collect column referen
                values.append(value)  # Collect values to filter by
            else:
                raise InvalidRequestError(f"Invalid attribute: {key}")

        # Query the database
        result = self._session.query(User).filter(
            tuple_(*columns).in_([tuple(values)])
        ).first()

        # Raise error if no user is found
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database by their user ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The key-value pairs of attributes to update.

        Raises:
            ValueError: If an invalid attribute is provided in kwargs.
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        # Prepare the update dictionary
        update_data = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_data[getattr(User, key)] = value  # Collect valid
            else:
                raise ValueError(f"Invalid attribute: {key}")

        # Update the user record
        self._session.query(User).filter(User.id == user_id).update(
            update_data,
            synchronize_session=False,
        )
        self._session.commit()
