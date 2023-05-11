from django.db import models
from apps.website.models import CustomUser
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


