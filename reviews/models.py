from django.db import models
from django.conf import settings
from catalog.models import Product
# Create your models here.

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveIntegerField()
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
