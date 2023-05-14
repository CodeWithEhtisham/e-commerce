from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    

class AddToCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('adminpanel.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)