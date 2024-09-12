#!/usr/bin/env python3
"""
The `user` module defines the `User` model, representing the structure of
the `users` table in the application's database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Define the base class for all models using SQLAlchemy's ORM
Base = declarative_base()


class User(Base):
    """
    Represents a user in the application.

    This class maps to the `users` table in the database and stores user-related
    information such as email, hashed password, session ID, and reset token.
    """
    
    __tablename__ = "users"  # Name of the table in the database

    # Define the columns for the `users` table
    id = Column(Integer, primary_key=True)  # Primary key, unique user ID
    email = Column(String(250), nullable=False)  # User's email address, cannot be null
    hashed_password = Column(String(250), nullable=False)  # Hashed password for security
    session_id = Column(String(250), nullable=True)  # Session ID for tracking user sessions (optional)
    reset_token = Column(String(250), nullable=True)  # Token for password reset functionality (optional)
