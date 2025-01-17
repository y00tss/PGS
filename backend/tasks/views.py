from rest_framework import viewsets
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django.core.cache import cache


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'created_at']
    ordering_fields = ['priority', 'created_at']

    def get_queryset(self):
        user = self.request.user
        cache_key = f"user_{user.id}_tasks"
        cached_tasks = cache.get(cache_key)

        if cached_tasks is not None:
            return cached_tasks

        tasks = self.queryset.filter(user=user)
        cache.set(cache_key, tasks, timeout=60)
        return tasks

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        cache.delete(f"user_{self.request.user.id}_tasks")
        return task

    def perform_update(self, serializer):
        task = serializer.save()
        cache.delete(f"user_{self.request.user.id}_tasks")
        return task

    def perform_destroy(self, instance):
        cache.delete(f"user_{self.request.user.id}_tasks")
        instance.delete()
