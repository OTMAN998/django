from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='cv_dashboard'),
    path('create/', views.cv_create, name='cv_create'),
    path('<int:pk>/', views.cv_detail, name='cv_detail'),
    path('<int:cv_id>/add-experience/', views.add_experience, name='add_experience'),
]
