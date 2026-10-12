import pytest

from app import create_app
from app.database import db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def register_user(client):
    def _register(email="tope@example.com", password="secret123", name="Tope", phone_number="08012345678"):
        return client.post(
            "/user/register",
            json={"name": name, "email": email, "password": password, "phone_number": phone_number},
        )

    return _register


@pytest.fixture
def auth_headers(client, register_user):
    def _headers(email="tope@example.com", password="secret123"):
        register_user(email=email, password=password)
        response = client.post("/user/login", json={"email": email, "password": password})
        return {"Authorization": f"Bearer {response.get_json()['access_token']}"}

    return _headers
