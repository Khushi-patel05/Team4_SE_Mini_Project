import pytest

import app as app_module


@pytest.fixture
def app(tmp_path):
    """Use an isolated temporary database for every test."""
    app_module.app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        DATABASE=str(tmp_path / "test_healthcare.db"),
    )

    app_module.initialize_database()

    yield app_module.app


@pytest.fixture
def client(app):
    """Provide an authenticated Flask test client."""
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "Administrator"

    return client


@pytest.fixture
def patient_data():
    """Valid patient registration details."""
    return {
        "full_name": "Test Patient",
        "date_of_birth": "1990-05-15",
        "gender": "Female",
        "phone": "9876543210",
        "email": "test.patient@example.com",
        "address": "Test Address",
    }