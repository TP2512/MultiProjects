from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Not Authorised"}


def test_successful_login():
    # Assuming your authentication endpoint is /login and accepts POST requests with username and password
    response = client.post("/login", data={"username": "Tarkesh_2512", "password": "Tarkesh_251293"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_invalid_credentials():
    response = client.post("/login", data={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_missing_credentials():
    response = client.post("/login", data={})
    assert response.status_code == 422
    assert response.json() == {"detail": [{"type": "missing", "loc": ["body", "username"], "msg": "Field required",
                                           "input":None, "url": "https://errors.pydantic.dev/2.6/v/missing"},
                                          {"type": "missing", "loc": ["body", "password"], "msg": "Field required",
                                           "input": None, "url":"https://errors.pydantic.dev/2.6/v/missing"}]}

