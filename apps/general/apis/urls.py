from django.urls import path
from . import views

app_name = "general"

urlpatterns = [
    path('service-list/', views.ServiceListView.as_view()),
    path('service-detail/<int:id>/', views.ServiceUpdateView.as_view()),
    path('service-options/', views.ServiceOptionView.as_view()),
    path('designation-list/', views.DesignationView.as_view()),
    path('designation-detail/<int:id>/', views.DesignationDetailView.as_view())
]