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
    
class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stockins')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            creating = self._state.adding
            super().save(*args, **kwargs)
            if creating:
                # update product stock and moving average cost
                p = self.product
                old_stock = p.stock
                old_avg = p.avg_cost
                new_qty = self.quantity
                new_cost = self.unit_cost
                total_cost = old_stock * old_avg + new_qty * new_cost
                new_stock = old_stock + new_qty
                p.stock = new_stock
                p.avg_cost = (total_cost / new_stock) if new_stock > 0 else 0
                p.purchase_price = new_cost
                p.save()

class StockOut(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stockouts')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_basis = models.DecimalField(max_digits=12, decimal_places=4, editable=False, default=0)
    date = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            creating = self._state.adding
            if creating:
                # snapshot current avg_cost before changing stock
                self.cost_basis = self.product.avg_cost
            super().save(*args, **kwargs)
            if creating:
                p = self.product
                if self.quantity > p.stock:
                    raise ValueError("Insufficient stock")
                p.stock = p.stock - self.quantity
                p.save()

    @property
    def profit(self):
        return (self.unit_price - self.cost_basis) * self.quantity