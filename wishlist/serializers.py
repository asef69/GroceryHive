
from rest_framework import serializers
from .models import WishlistItem
from catalog.serializers import ProductSerializer
from catalog.models import Product

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    class Meta:
        model = WishlistItem
        fields = ("id","product","product_id")
