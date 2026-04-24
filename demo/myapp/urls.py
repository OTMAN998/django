from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("todos/", views.todos, name="todos"),
    path('', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('activate/<str:token>/', views.activate, name='activate'),
]