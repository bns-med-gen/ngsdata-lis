"""
URL configuration for lis project.
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
    path('', include('lis_auth.urls')),
]
