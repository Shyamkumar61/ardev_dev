from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('client-list/', views.ClientListView.as_view(), name='client-list'),
    path('client-filter-list/', views.ClientFilterView.as_view(), name='client-filtered-list'),
    path('client-detail/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('create-client/', views.ClientCreateView.as_view()),
    path('emp-shift/', views.EmployeeShiftView.as_view()),
    path('emp-shift-list/', views.ShiftEmployeeList.as_view()),
    path('emp_reassing/<int:pk>/', views.ShiftEmployeeDetails.as_view()),
    path('client-option-list/', views.ClientOptionView.as_view()),
    path('client-emp-list/<int:pk>/', views.ClientEmpListView.as_view())
]
