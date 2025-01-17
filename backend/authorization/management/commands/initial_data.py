from django.core.management.base import BaseCommand
from authorization.models import User
from tasks.models import Task


class Command(BaseCommand):
    help = 'Load initial data into the database during the first run'

    def handle(self, *args, **kwargs):
        self.create_user()
        self.create_tasks()

    def create_user(self):
        """SuperAdmin add"""

        check_user = User.objects.filter(email='admin@admin.com')
        if not check_user:
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin'
            )
            self.stdout.write("Superuser created", ending="")

    def create_tasks(self):
        """Tasks add for superuser"""

        admin = User.objects.get(email='admin@admin.com')

        tasks_data = [
            {'title': 'Настроить сервер', 'description': 'Настроить окружение для проекта', 'priority': 'high'}, # noqa
            {'title': 'Обновить документацию', 'description': 'Добавить API эндпоинты', 'priority': 'medium'}, # noqa
            {'title': 'Проверить тесты', 'description': 'Реализовать вебхуки', 'priority': 'low'}, # noqa
            {'title': 'Создать новую задачу', 'description': 'Добавить Редис для кэширования', 'priority': 'high'}, # noqa
            {'title': 'Провести ревью кода', 'description': 'Провести ревью кода перед релизом', 'priority': 'medium'}, # noqa
        ]

        for task in tasks_data:
            Task.objects.get_or_create(user=admin, **task)

        self.stdout.write(self.style.SUCCESS("Test tasks created"))
