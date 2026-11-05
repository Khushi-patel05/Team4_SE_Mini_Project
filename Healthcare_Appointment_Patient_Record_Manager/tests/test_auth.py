
import sqlite3

import pytest
from werkzeug.security import check_password_hash

from auth import create_user, initialize_auth_database


@pytest.fixture(autouse=True)
def setup_auth_database(app):
    """Initialize the authentication database for every test."""
    with app.app_context():
        initialize_auth_database()


def test_create_user_rejects_short_password(app):
    with app.app_context():
        with pytest.raises(
            ValueError,
            match="Password must contain at least 8 characters."
        ):
            create_user("shortpass", "abc123", "Doctor")


def test_create_user_accepts_valid_password(app):
    with app.app_context():
        create_user("validuser", "securepass123", "Doctor")

        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row

        try:
            user = connection.execute(
                """
                SELECT username, password_hash, role
                FROM users
                WHERE username = ?
                """,
                ("validuser",)
            ).fetchone()
        finally:
            connection.close()

        assert user is not None
        assert user["username"] == "validuser"
        assert user["role"] == "Doctor"
        assert check_password_hash(user["password_hash"], "securepass123")


def test_create_user_rejects_empty_username(app):
    with app.app_context():
        with pytest.raises(
            ValueError,
            match="Username and password are required."
        ):
            create_user("", "securepass123", "Doctor")


def test_create_user_rejects_invalid_role(app):
    with app.app_context():
        with pytest.raises(
            ValueError,
            match="Invalid user role."
        ):
            create_user("invalidrole", "securepass123", "Patient")
