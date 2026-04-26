from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='cv_dashboard'),
    path('create/', views.cv_create, name='cv_create'),
    path('<int:pk>/', views.cv_detail, name='cv_detail'),
    path('<int:pk>/edit/', views.cv_edit, name='cv_edit'),
    path('<int:pk>/pdf/', views.generate_pdf_cv, name='generate_pdf_cv'),
    path('<int:pk>/delete/', views.cv_delete, name='cv_delete'),

    # Expérience
    path('<int:cv_id>/add-experience/', views.add_experience, name='add_experience'),
    path('experience/<int:pk>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),

    # Formation
    path('<int:cv_id>/add-education/', views.add_education, name='add_education'),
    path('education/<int:pk>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:pk>/delete/', views.delete_education, name='delete_education'),

    # Compétence
    path('<int:cv_id>/add-skill/', views.add_skill, name='add_skill'),
    path('skill/<int:pk>/edit/', views.edit_skill, name='edit_skill'),
    path('skill/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    # Langue
    path('<int:cv_id>/add-language/', views.add_language, name='add_language'),
    path('language/<int:pk>/edit/', views.edit_language, name='edit_language'),
    path('language/<int:pk>/delete/', views.delete_language, name='delete_language'),
]
