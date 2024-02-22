#!/usr/bin/env python3
"""Integration tests"""
import requests


URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
    Test register a user with the given email and password.
    """
    response = requests.post(f'{URL}/users',
                             data={'email': email, 'password': password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test logs in with a wrong password
    """
    response = requests.post(f'{URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test log in with correct email and password
    """
    response = requests.post(f'{URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """
    Test unlogged user profile access
    """
    response = requests.get(f'{URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test profile access after a successful login
    """
    response = requests.get(f'{URL}/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Test logging out the user
    """
    response = requests.delete(f'{URL}/sessions',
                               cookies={'session_id': session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test reset the password token for a given email
    """
    response = requests.post(f'{URL}/reset_password',
                             data={'email': email})
    assert response.status_code == 200
    reset_token = response.json()['reset_token']
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test updating a user's password
    """
    response = requests.put(f'{URL}/reset_password',
                            data={'email': email, 'reset_token': reset_token,
                                  'new_password': new_password})
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
