import pytest  # noqa
from authorization.models import User


def test_register_user_success(client):
    data = {
        "email": "test@test.com",
        "password": "test123",
        "username": "test"
    }
    response = client.post("/auth/register/", data)
    assert response.status_code == 201
    assert User.objects.filter(email="test@test.com").exists()


def test_register_user_fail(client, user):
    """The same user already exists"""
    data = {
        "email": "test@test.com",
        "password": "test123",
        "username": "test"
    }
    response = client.post("/auth/register/", data)
    assert response.status_code == 400


def test_login_user_success(client, user):
    data = {
        "email": "test@test.com",
        "password": "test123"
    }
    response = client.post("/auth/login/", data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


def test_login_user_fail(client, user):
    data = {
        "email": "test@test.com",
        "password": "test15465464564564523"
    }
    response = client.post("/auth/login/", data)
    assert response.status_code == 400


def test_profile_view_success(client, user):
    client.force_authenticate(user=user)
    response = client.get("/auth/profile/")
    assert response.status_code == 200
    assert response.data["email"] == "test@test.com"
