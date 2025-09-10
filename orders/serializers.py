from rest_framework import serializers
from .models import Order,OrderItem,CartItem
from catalog.serializers import ProductSerializer
from catalog.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),source='product',write_only=True)
    class Meta:
        model=CartItem
        fields=['id','product','product_id','quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields=['seller','product','quantity','price']


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=['id','created_at','total_amount','items']