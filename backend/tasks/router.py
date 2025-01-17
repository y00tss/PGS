from tasks import views as task_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", task_views.TaskViewSet, basename="tasks")

urlpatterns = router.urls
