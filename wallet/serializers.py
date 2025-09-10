from rest_framework import serializers
from .models import Wallet,Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields=['balance']


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2,min_value=0.01)
