"""
Django URL Configuration for LeakGPT Naija Pro
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/analytics/', include('django_app.analytics.urls')),
    path('api/reports/', include('django_app.reports.urls')),
]