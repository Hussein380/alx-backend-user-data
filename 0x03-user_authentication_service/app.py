#!/usr/bin/env python3
"""
A simple Flask app that supports user authentication features
such as user registration, login, profile viewing, session management,
and password reset functionality.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth  # Import the authentication handler

app = Flask(__name__)  # Initialize the Flask app
AUTH = Auth()  # Create an instance of the Auth class for managing user auth


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    The homepage of the app, welcoming users.
    Returns:
        A JSON message to welcome users to the app.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    POST /users
    Endpoint to register a new user with email and password.

    - Expects 'email' and 'password' from the form data.
    - If registration is successful, returns a message with user email.
    - If the email is already registered, returns an error message.

    Returns:
        JSON response indicating successful user creation or an error.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Endpoint for user login.

    - Expects 'email' and 'password' from the form data.
    - If the login credentials are valid, creates a new session for the user
      and sets a session cookie with the session ID.
    - If invalid, returns a 401 error (unauthorized).

    Returns:
        A JSON response with a login success message, including
        the session cookie.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)  # If login is invalid, return a 401 Unauthorized error
    session_id = AUTH.create_session(email)  # Create a session for the user
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)  # Set session cookie
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    DELETE /sessions
    Endpoint for logging out a user.

    - Retrieves the session ID from the cookies.
    - If the session exists, the session is destroyed and the user
    is logged out.
    - If no session is found, a 403 error (forbidden) is returned.

    Returns:
        Redirects the user back to the homepage after logging out.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # If no valid session, return a 403 Forbidden error
    AUTH.destroy_session(user.id)  # Destroy the session
    return redirect("/")  # Redirect the user to the homepage


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET /profile
    Endpoint to view the user's profile.

    - Retrieves the session ID from cookies.
    - If the session is valid, returns the user's email.
    - If the session is invalid, returns a 403 error.

    Returns:
        JSON response containing the user's email or a 403 error.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # If no valid session, return a 403 Forbidden error

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Endpoint to request a password reset token.

    - Expects 'email' from the form data.
    - If the email is valid, a reset token is generated and returned.
    - If the email is invalid, a 403 error is returned.

    Returns:
        JSON response containing the reset token or a 403 error.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)  # If the email is invalid, return a 403 Forbidden error

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Endpoint to update a user's password using a reset token.

    - Expects 'email', 'reset_token', and 'new_password' from the form data.
    - If the reset token is valid, updates the password and returns a success
    message.
    - If the reset token is invalid or update fails, returns a 403 error.

    Returns:
        JSON response indicating success or failure in updating the password.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)  # If the reset token is invalid, return a 403

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
