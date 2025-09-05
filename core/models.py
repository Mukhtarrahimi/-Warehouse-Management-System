from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.ADMIN)