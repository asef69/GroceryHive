from rest_framework import serializers
from .models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']


class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category',write_only=True)
    class Meta:
        model=Product
        fields = ("id","name","description","category","category_id","price","stock","is_active","seller","created_at")
        read_only_fields=['seller','created_at']
