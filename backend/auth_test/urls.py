from django.urls import path
from .views import LoginView, TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_test_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_test_refresh'),
]
