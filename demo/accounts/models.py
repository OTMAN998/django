from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'Utilisateur'

    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
