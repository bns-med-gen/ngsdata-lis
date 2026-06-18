"""
URL configuration for lis_api project.
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
    path('auth/', include('auth_test.urls')),
]
