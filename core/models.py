from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.ADMIN)

class Supplier(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name
