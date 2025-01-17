from django.db import models
from authorization.models import User


class Task(models.Model):
    """Task model"""
    STATUS_CHOICES = (
        ('new', 'New'),
        ('pending', 'In Progress'),
        ('completed', 'Completed')
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
