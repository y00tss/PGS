import pytest  # noqa
from authorization.models import User
from django.core.exceptions import ValidationError


def test_create_user_without_email_fail(client):
    with pytest.raises(ValidationError):
        User.objects.create(
            password="test123",
            first_name="Test",
            last_name="Test"
        )


def test_create_user_success(client):
    user = User.objects.create(
        email="test1@test.com",
        password="test123",
        username="test1"
    )
    assert user.email == "test1@test.com"
    assert user.username == "test1"
    assert user.is_active
    assert ~user.is_staff


def test_create_user_with_same_email_fail(client):
    User.objects.create(
        email="test1@test.com",
        password="test123",
        username="test1"
    )
    with pytest.raises(ValidationError):
        User.objects.create(
            email="test1@test.com",
            password="test123",
            username="test2"
        )


def test_create_superuser_success(client):
    user = User.objects.create_superuser(
        email="admin@test.com",
        password="admin123",
        username="admin"
    )
    assert user.is_superuser
    assert user.is_staff
    assert user.is_active


def test_invalid_email_fail(client):
    with pytest.raises(ValidationError):
        user = User(email="invalid-email", password="test123", username="test")
        user.full_clean()


def test_update_user_success(user):
    user.is_staff = True
    user.save()
    assert user.is_staff


def test_update_user_password_success(user):
    user.set_password("newpassword123")
    user.save()
    assert user.check_password("newpassword123")


def test_delete_user_success(user):
    user.delete()
    assert User.objects.count() == 0


def test_user_str_representation_success(user):
    assert str(user) == user.email


def test_user_verbose_name_success():
    assert User._meta.verbose_name == "Администратор"
    assert User._meta.verbose_name_plural == "Администраторы"
