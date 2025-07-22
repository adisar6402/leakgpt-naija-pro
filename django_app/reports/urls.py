from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentReportViewSet, ScamReportEnhancedViewSet, TrendAnalysisViewSet

router = DefaultRouter()
router.register(r'documents', DocumentReportViewSet)
router.register(r'scams', ScamReportEnhancedViewSet)
router.register(r'trends', TrendAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]