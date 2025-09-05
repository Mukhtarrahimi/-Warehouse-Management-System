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

class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=60, unique=True)
    category = models.CharField(max_length=80, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # last purchase price
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)      # default sale price
    stock = models.IntegerField(default=0)
    avg_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)        # moving average cost
    low_stock_threshold = models.IntegerField(default=5)
    def __str__(self):
        return f"{self.name} ({self.code})"