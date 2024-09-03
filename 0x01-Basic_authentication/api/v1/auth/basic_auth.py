#!/usr/bin/env python3
""" Basic authentication module for the API """

import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication class """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header

        Args:
            authorization_header (str): The full Authorization header

        Returns:
            str: The Base64 encoded string, or None if the input is invalid
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 string into a UTF-8 string

        Args:
            base64_authorization_header (str): The Base64 encoded string

        Returns:
            str: The decoded string, or None if the input is invalid or
            decoding fails
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user email and password from the decoded Base64 string

        Args:
            decoded_base64_authorization_header (str): The decoded Base64

        Returns:
            tuple: A tuple containing the user email and password, or
            (None, None) if the input is invalid
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieves the User instance based on email and password

        Args:
            user_email (str): The user's email
            user_pwd (str): The user's password

        Returns:
            User: The User instance if found and password matches,
            otherwise None
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for the request

        Args:
            request: The HTTP request object

        Returns:
            User: The User instance if authenticated, otherwise None
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_part = self.extract_base64_authorization_header(auth_header)
        if not base64_part:
            return None
        decoded_str = self.decode_base64_authorization_header(base64_part)
        if not decoded_str:
            return None
        email, password = self.extract_user_credentials(decoded_str)
        if not email or not password:
            return None
        return self.user_object_from_credentials(email, password)
