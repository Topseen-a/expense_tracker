def test_register_user(register_user):
    response = register_user()

    assert response.status_code == 201
    body = response.get_json()
    assert body["email"] == "tope@example.com"
    assert "password" not in body


def test_register_normalizes_email(register_user):
    response = register_user(email="  Tope@Example.COM ")

    assert response.status_code == 201
    assert response.get_json()["email"] == "tope@example.com"


def test_register_duplicate_email_returns_409(register_user):
    register_user()
    response = register_user()

    assert response.status_code == 409
    assert response.get_json() == {"error": "Email already exists"}


def test_register_validation_errors(client):
    response = client.post(
        "/user/register",
        json={"name": "", "email": "bad", "phone_number": "123", "password": "x"},
    )

    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert set(errors) == {"name", "email", "phone_number", "password"}


def test_register_without_json_body_returns_400(client):
    response = client.post("/user/register", data="not json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be a JSON object"


def test_login_success(client, register_user):
    register_user()
    response = client.post("/user/login", json={"email": "tope@example.com", "password": "secret123"})

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_wrong_password_returns_401(client, register_user):
    register_user()
    response = client.post("/user/login", json={"email": "tope@example.com", "password": "wrong-pass"})

    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/user/me")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authorization token is missing"}


def test_get_and_update_me(client, auth_headers):
    headers = auth_headers()

    assert client.get("/user/me", headers=headers).get_json()["name"] == "Tope"

    response = client.put("/user/me", json={"name": "Temitope"}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["name"] == "Temitope"


def test_update_me_validates_input(client, auth_headers):
    response = client.put("/user/me", json={"phone_number": "abc"}, headers=auth_headers())

    assert response.status_code == 400
    assert "phone_number" in response.get_json()["errors"]


def test_delete_me(client, auth_headers):
    headers = auth_headers()

    assert client.delete("/user/me", headers=headers).status_code == 200
    assert client.get("/user/me", headers=headers).status_code == 404
