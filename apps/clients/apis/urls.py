from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('client-list/', views.ClientListView.as_view(), name='client-list'),
    path('client-detail/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('create-client/', views.ClientCreateView.as_view()),
    path('emp-shift/', views.EmployeeShiftSerializer.as_view()),
    path('emp-shift-list/', views.ShiftEmployeeList.as_view()),
    path('client-option-list/', views.ClientOptionView.as_view())
]
