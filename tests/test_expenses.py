import pytest


@pytest.fixture
def headers(auth_headers):
    return auth_headers()


def create_expense(client, headers, **overrides):
    payload = {"amount": 1500.50, "category": "Food", **overrides}
    return client.post("/expense/", json=payload, headers=headers)


def test_create_expense(client, headers):
    response = create_expense(client, headers)

    assert response.status_code == 201
    body = response.get_json()
    assert body["amount"] == 1500.50
    assert body["category"] == "Food"


def test_create_expense_with_date(client, headers):
    response = create_expense(client, headers, date="2026-01-15")

    assert response.status_code == 201
    assert response.get_json()["date"].startswith("2026-01-15")


@pytest.mark.parametrize(
    "amount, message",
    [
        (None, "Amount is required"),
        ("abc", "Amount must be a number"),
        (True, "Amount must be a number"),
        (0, "Amount must be greater than 0"),
        (-5, "Amount must be greater than 0"),
        (1.234, "Amount cannot have more than 2 decimal places"),
    ],
)
def test_create_expense_invalid_amount(client, headers, amount, message):
    response = create_expense(client, headers, amount=amount)

    assert response.status_code == 400
    assert response.get_json()["errors"]["amount"] == message


def test_list_expenses_only_returns_own(client, auth_headers):
    mine = auth_headers()
    theirs = auth_headers(email="other@example.com")
    create_expense(client, mine)
    create_expense(client, theirs)

    response = client.get("/expense/", headers=mine)

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_expense_not_found(client, headers):
    response = client.get("/expense/999", headers=headers)

    assert response.status_code == 404
    assert response.get_json() == {"error": "Expense not found"}


def test_update_expense(client, headers):
    expense_id = create_expense(client, headers).get_json()["id"]

    response = client.put(f"/expense/{expense_id}", json={"amount": 20, "category": "Transport"}, headers=headers)

    assert response.status_code == 200
    assert response.get_json()["amount"] == 20
    assert response.get_json()["category"] == "Transport"


def test_update_expense_invalid_returns_400(client, headers):
    expense_id = create_expense(client, headers).get_json()["id"]

    response = client.put(f"/expense/{expense_id}", json={"amount": -1}, headers=headers)

    assert response.status_code == 400


def test_delete_own_expense(client, headers):
    expense_id = create_expense(client, headers).get_json()["id"]

    assert client.delete(f"/expense/{expense_id}", headers=headers).status_code == 200
    assert client.get(f"/expense/{expense_id}", headers=headers).status_code == 404


def test_cannot_touch_another_users_expense(client, auth_headers):
    owner = auth_headers()
    intruder = auth_headers(email="intruder@example.com")
    expense_id = create_expense(client, owner).get_json()["id"]

    assert client.get(f"/expense/{expense_id}", headers=intruder).status_code == 403
    assert client.put(f"/expense/{expense_id}", json={"amount": 1}, headers=intruder).status_code == 403
    assert client.delete(f"/expense/{expense_id}", headers=intruder).status_code == 403


def test_filter_by_category(client, headers):
    create_expense(client, headers, category="Food")
    create_expense(client, headers, category="Rent")

    response = client.get("/expense/filter/category?category=Food", headers=headers)

    assert [e["category"] for e in response.get_json()] == ["Food"]


def test_filter_by_category_requires_param(client, headers):
    assert client.get("/expense/filter/category", headers=headers).status_code == 400


def test_filter_by_date_end_date_is_inclusive(client, headers):
    create_expense(client, headers, date="2026-03-01T00:00:00")
    create_expense(client, headers, date="2026-03-31T18:30:00")
    create_expense(client, headers, date="2026-04-01T00:00:00")

    response = client.get("/expense/filter/date?start_date=2026-03-01&end_date=2026-03-31", headers=headers)

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_filter_by_date_invalid_returns_400(client, headers):
    response = client.get("/expense/filter/date?start_date=bad&end_date=2026-03-31", headers=headers)

    assert response.status_code == 400


def test_monthly_summary(client, headers):
    create_expense(client, headers, amount=100.25, date="2026-05-02")
    create_expense(client, headers, amount=50.25, date="2026-05-20")
    create_expense(client, headers, amount=999, date="2026-06-01")

    response = client.get("/expense/summary/monthly?year=2026&month=5", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["total_expense"] == 150.50


def test_monthly_summary_invalid_month(client, headers):
    response = client.get("/expense/summary/monthly?year=2026&month=13", headers=headers)

    assert response.status_code == 400


def test_unknown_route_returns_json_404(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}
