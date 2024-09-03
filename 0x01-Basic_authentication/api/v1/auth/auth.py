#!/usr/bin/env python3
""" Base authentication class """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Base class for authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the path requires authentication

        Args:
            path (str): The request path
            excluded_paths (List[str]): List of paths that do not require
            authentication

        Returns:
            bool: True if the path requires authentication, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        return not any(path.startswith(excluded_path)
                       for excluded_path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Gets the value of the Authorization header from the request

        Args:
            request: The HTTP request object

        Returns:
            str: The value of the Authorization header, or None if not present
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on the request

        Args:
            request: The HTTP request object

        Returns:
            User: The current user, or None if not authenticated
        """
        return None
