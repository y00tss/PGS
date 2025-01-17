import pytest
from authorization.models import User
from rest_framework.test import APIClient
from tasks.models import Task


@pytest.fixture
def user(client):
    return User.objects.create_user(
        email='test@test.com',
        password='test123',
        username="test"
    )


@pytest.fixture
def additional_user(client):
    return User.objects.create_user(
        email='test10@test.com',
        password='test123',
        username="test10"
    )


@pytest.fixture
def client(db):
    """API Fixture"""
    return APIClient()


@pytest.fixture
def task(user):
    return Task.objects.create(
        title="Test Task",
        description="Test Task Description",
        status='new',
        priority='low',
        user=user
    )
