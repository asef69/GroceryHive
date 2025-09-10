from django.db import models
from django.conf import settings
from catalog.models import Product
# Create your models here.

class WishlistItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
