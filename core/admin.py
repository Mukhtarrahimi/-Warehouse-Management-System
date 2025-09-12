
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Supplier, Customer, Product, StockIn, StockOut

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)
    list_display = ('username','email','role','is_staff','is_superuser')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name','phone')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','code','category','stock','avg_cost','sale_price')
    search_fields = ('name','code','category')

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','unit_cost','date','supplier')

@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','unit_price','cost_basis','date','customer')
