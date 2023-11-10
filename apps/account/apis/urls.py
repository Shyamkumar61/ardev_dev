from django.urls import path
from .views import RegisterUserView, LoginView

app_name = 'account'

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login-user')
]
