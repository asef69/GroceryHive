from django.shortcuts import render
from decimal import Decimal
from rest_framework import generics,permissions,status,viewsets
from rest_framework.response import Response
from .models import Order,OrderItem,CartItem
from .serializers import OrderSerializer,CartItemSerializer
from catalog.models import Product
from wallet.models import Wallet,Transaction
from core.emails import send_order_email
from django.db import transaction
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
# Create your views here.

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self): # type: ignore
        return CartItem.objects.filter(user=self.request.user).select_related('product','product__category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # type: ignore


class CheckoutView(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs): # type: ignore
        user=request.user
        cart=CartItem.objects.filter(user=user).select_related('product','product__seller')
        if not cart.exists():
            return Response({'detail':'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        total=Decimal('0.00')
        for ci in cart:
            if not ci.product.is_active or ci.product.stock<ci.quantity:
                return Response({'detail':f'Product {ci.product.name} is not available'},status=status.HTTP_400_BAD_REQUEST)
            total+=ci.product.price*ci.quantity
        wallet=user.wallet
        if wallet.balance<total:
            return Response({'detail':'Insufficient balance in wallet'},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order=Order.objects.create(user=user,total_amount=total)
            for ci in cart:
                OrderItem.objects.create(
                    order=order,
                    seller=ci.product.seller,
                    product=ci.product,
                    quantity=ci.quantity,
                    price=ci.product.price
                )
                ci.product.stock-=ci.quantity
                ci.product.save()
            wallet.balance-=total
            wallet.save()
            Transaction.objects.create(wallet=wallet,type='PURCHASE',amount=total)
            cart.delete()

        send_order_email(user.email,order.id,float(order.total_amount)) # type: ignore
        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)



class PurchaseHistoryView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer

    def get_queryset(self): # type: ignore
        return Order.objects.filter(user=self.request.user).prefetch_related('items','items__product')
    

class SellerDashboardView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer

    def list(self, request, *args, **kwargs):
        if request.user.role!='seller' and not request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to access this resource.") # type: ignore
        ITEMS=OrderItem.objects.filter(seller=request.user).select_related('order','product')
        data=[{
            'order_id':oi.order_id, # type: ignore
            'product':oi.product.name if oi.product else 'Deleted Product',
            'quantity':oi.quantity,
            'price':str(oi.price),
        } for oi in ITEMS]
        return Response({'seller':request.user.email,'sales':data}) # type: ignore
    

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Customer can only see their own orders; admin can see all."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all().prefetch_related("items","items__product")
        return Order.objects.filter(user=user).prefetch_related("items","items__product")

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Nested under /orders/{order_pk}/items/"""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        order_pk = self.kwargs.get("order_pk")
        qs = OrderItem.objects.filter(order_id=order_pk).select_related("order","product")
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        if not Order.objects.filter(id=order_pk, user=self.request.user).exists():
            raise PermissionDenied("Not your order.")
        return qs