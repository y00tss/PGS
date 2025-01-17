import pytest  # noqa
from tasks.models import Task
from django.core.exceptions import ValidationError


def test_create_task_without_title(user):
    with pytest.raises(ValidationError):
        Task.objects.create(
            description="This is a new task",
            status='new',
            priority='low',
            user=user
        )


def test_create_task_success(user):
    task = Task.objects.create(
        title="New Task",
        description="This is a new task",
        status='new',
        priority='low',
        user=user
    )
    assert task.title == "New Task"
    assert task.description == "This is a new task"
    assert task.status == 'new'
    assert task.priority == 'low'
    assert task.user == user


def test_create_task_with_wrong_status_fail(user):
    with pytest.raises(ValidationError):
        Task.objects.create(
            title="New Task",
            description="This is a new task",
            status='wrong_status',
            priority='lowwss',
            user=user
        )


def test_task_status_choices_success(task):
    assert task.status == 'new'
    task.status = 'completed'
    task.save()
    assert task.status == 'completed'


def test_task_status_choices_fail(task):
    with pytest.raises(ValidationError):
        task.status = 'wrong_status'
        task.save()


def test_task_priority_choices_success(task):
    assert task.priority == 'low'
    task.priority = 'high'
    task.save()
    assert task.priority == 'high'
