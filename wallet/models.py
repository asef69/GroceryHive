from django.db import models
from django.conf import settings
from decimal import Decimal
# Create your models here.

class Wallet(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wallet')
    balance=models.DecimalField(max_digits=12,decimal_places=2,default=Decimal('0.00'))



class Transaction(models.Model):
    TYPES=[
        ('DEPOSIT','Deposit'),
        ('PURCHASE','Purchase'),
    ]
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='transactions')
    type=models.CharField(max_length=10,choices=TYPES)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

