from django.db import models
from django.conf import settings
from catalog.models import Product
# Create your models here.

class CartItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart_items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

   

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=12,decimal_places=2)



class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=12,decimal_places=2)
    seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='sold_items')
