#!/usr/bin/env python3
"""Route module for the API.

This module sets up the Flask application, handles routing, and manages
authentication for the API. It also includes error handlers for common HTTP
errors such as 404, 401, and 403.
"""

import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

# Initialize the Flask application
app = Flask(__name__)

# Register the blueprint for application views
app.register_blueprint(app_views)

# Enable CORS for all routes under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the authentication variable
auth = None

# Determine the authentication type from environment variables
auth_type = getenv('AUTH_TYPE', 'auth')

# Instantiate the appropriate authentication class based on AUTH_TYPE
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """Handle 404 Not Found errors.

    Returns a JSON response with a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handle 401 Unauthorized errors.

    Returns a JSON response with a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Handle 403 Forbidden errors.

    Returns a JSON response with a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def authenticate_user():
    """Authenticate a user before processing a request.

    This function is called before every request to ensure the user is
    authenticated. It checks if the request path requires authentication
    and verifies the authorization header and current user.
    """
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            if auth_header is None:
                abort(401)  # Abort with 401 Unauthorized if no auth header
            if user is None:
                abort(403)  # Abort with 403 Forbidden if no valid user


if __name__ == "__main__":
    # Get the host and port from environment variables, with defaults
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
