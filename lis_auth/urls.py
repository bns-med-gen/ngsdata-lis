from django.urls import path
from .views import LoginView, TokenRefreshView, index, select_login_method, accept_token

urlpatterns = [
    path('admlogin/', LoginView.as_view(), name='adm_login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('', index, name="index"),
    path('select_login_method', select_login_method, name="select_login_method"),
    path('accept_token', accept_token, name="accept_token"),

]
