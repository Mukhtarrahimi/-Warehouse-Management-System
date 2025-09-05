from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Supplier, Customer, StockIn, StockOut

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','code','category','purchase_price','sale_price','low_stock_threshold']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name','phone','address']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','phone','address']