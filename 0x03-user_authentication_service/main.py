#!/usr/bin/env python3
"""End-to-end (E2E) integration tests for `app.py` to ensure user authentication functionalities work correctly.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Test user registration functionality.
    
    Attempts to register a new user and verifies:
    - The response status code is 200 and the correct message is returned.
    - If the same email is registered again, the response status code is 400 with an error message.
    """
    url = f"{BASE_URL}/users"
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    
    # Attempt to register the same user again
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login functionality with incorrect password.
    
    Attempts to log in with a wrong password and verifies:
    - The response status code is 401 (Unauthorized).
    """
    url = f"{BASE_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test successful login functionality.
    
    Logs in with correct credentials and verifies:
    - The response status code is 200 and the correct message is returned.
    - Returns the session ID from the cookies for further use.
    """
    url = f"{BASE_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test access to profile information without being logged in.
    
    Attempts to access the `/profile` endpoint without a session and verifies:
    - The response status code is 403 (Forbidden).
    """
    url = f"{BASE_URL}/profile"
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test access to profile information while logged in.
    
    Attempts to access the `/profile` endpoint with a valid session ID and verifies:
    - The response status code is 200.
    - The response contains the user's email.
    """
    url = f"{BASE_URL}/profile"
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Test logging out of a session.
    
    Sends a DELETE request to the `/sessions` endpoint to log out and verifies:
    - The response status code is 200.
    - The response contains a redirect message.
    """
    url = f"{BASE_URL}/sessions"
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Test requesting a password reset token.
    
    Sends a POST request to `/reset_password` to get a reset token and verifies:
    - The response status code is 200.
    - The response contains the user's email and a reset token.
    - Returns the reset token for further use.
    """
    url = f"{BASE_URL}/reset_password"
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating a user's password using a reset token.
    
    Sends a PUT request to `/reset_password` to update the password and verifies:
    - The response status code is 200.
    - The response confirms the password update.
    """
    url = f"{BASE_URL}/reset_password"
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    # Execute the tests
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
