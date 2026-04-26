from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path("", views.home, name="home"),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),
    path('', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('activate/<str:token>/', views.activate, name='activate'),
]