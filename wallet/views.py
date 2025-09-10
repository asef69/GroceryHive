from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from .serializers import WalletSerializer,DepositSerializer
from .models import Wallet,Transaction
# Create your views here.

class MyWalletView(generics.RetrieveAPIView):
    serializer_class=WalletSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet # type: ignore
    

class DepositView(generics.CreateAPIView):
    serializer_class=DepositSerializer
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True)
        amount=s.validated_data['amount']
        wallet=request.user.wallet
        wallet.balance+=amount
        wallet.save()
        Transaction.objects.create(wallet=wallet,type='DEPOSIT',amount=amount)
        return Response({'detail':'Deposited Successfully','balance':str(wallet.balance)},status=status.HTTP_200_OK)

