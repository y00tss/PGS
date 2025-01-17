from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task


def notify_task_status(instance):  # pragma: no cover
    user_id = instance.user.id
    channel_layer = get_channel_layer()
    room_name = f"user_{user_id}"

    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            "type": "task_status",
            "message": f"Task {instance.title} changed to {instance.status}"
        },
    )


@receiver(post_save, sender=Task)
def task_status_update(sender, instance, **kwargs):  # pragma: no cover
    notify_task_status(instance)
