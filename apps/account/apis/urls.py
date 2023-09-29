from django.urls import path
from .views import RegisterUserView, LoginAPIView


urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginAPIView.as_view(), name='login-user')
]
