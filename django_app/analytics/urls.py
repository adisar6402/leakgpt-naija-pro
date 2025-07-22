from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, SystemMetricsViewSet

router = DefaultRouter()
router.register(r'events', AnalyticsViewSet)
router.register(r'metrics', SystemMetricsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]