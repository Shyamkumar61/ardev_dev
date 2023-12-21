from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path('emp/', views.EmployeeView.as_view(), name="employee"),
    path('emp/<str:emp_id>/', views.EmployeeDetailsView.as_view(), name="employee-details"),
    path('emp-bank-create/', views.EmployeeBankCreateView.as_view()),
    path('emp-bank-details/<str:pk>/', views.EmployeeBankDetailView.as_view())
]
