from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='products',null=True,blank=True)  
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,related_name='products')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']
