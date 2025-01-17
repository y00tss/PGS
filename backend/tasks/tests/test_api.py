import pytest  # noqa


# from tasks.models import Task
# from django.core.cache import cache


def test_get_tasks_unauthorized(client):
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_task_get_should_return_empty_list(client, user):
    client.force_authenticate(user=user)
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.data['count'] == 0


def test_task_post_should_succeed(client, user, task):
    client.force_authenticate(user=user)
    task = client.get("/tasks/")
    assert task.status_code == 200
    assert task.data['count'] == 1


def test_task_post_succeed(client, user):
    client.force_authenticate(user=user)
    data = {
        "title": "Test Task",
        "description": "Test Task Description",
        "status": "new",
        "priority": "low",
        "user": user.id
    }
    response = client.post("/tasks/", data)
    assert response.status_code == 201
    assert response.data["title"] == "Test Task"
    assert response.data["description"] == "Test Task Description"


def test_task_post_should_fail(client, user):
    client.force_authenticate(user=user)
    data = {
        "title": "Test Task",
        "description": "Test Task Description",
        "status": "newssdwad",
        "priority": "low51365",
    }
    response = client.post("/tasks/", data)
    assert response.status_code == 400


def test_task_update_should_succeed(client, user, task):
    client.force_authenticate(user=user)
    data = {
        "title": "Test Task New",
        "description": "NEw",
        "status": "new",
        "priority": "low",
        "user": user.id
    }
    response = client.put(f"/tasks/{task.id}/", data)
    assert response.status_code == 200
    assert response.data["title"] == "Test Task New"
    assert response.data["description"] == "NEw"


def test_delete_task_should_succeed(client, user, task):
    client.force_authenticate(user=user)
    response = client.delete(f"/tasks/{task.id}/")
    assert response.status_code == 204


def test_delete_task_should_fail(client, user, task):
    client.force_authenticate(user=user)
    response = client.delete(f"/tasks/{5}/")
    assert response.status_code == 404
