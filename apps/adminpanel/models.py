from django.db import models
from apps.website.models import CustomUser,Customer
# Create your models here.
class Product(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    quantity=models.IntegerField()
    category=models.CharField(max_length=100)
    price=models.IntegerField()
    Image=models.ImageField(upload_to='product_images')
    types=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    description=models.TextField()
    size=models.CharField(max_length=100,default='M')
    color=models.CharField(max_length=100,default='red')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=10, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True,default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)