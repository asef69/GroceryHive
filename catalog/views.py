from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from users.permissions import IsSeller
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filterset_fields = ["category"]
    search_fields = ["name","description"]
    ordering_fields = ["price","created_at"]

    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self): # type: ignore
        qs = Product.objects.all()
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            qs = qs.filter(category_id=category_pk)

        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return qs
        if user.is_authenticated and getattr(user, "role", None) == "seller":
            return qs.filter(Q(is_active=True) | Q(seller=user))
        return qs.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        seller = user if (user.is_authenticated and getattr(user, "role", None) == "seller") else None

        # If nested under category, attach it
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            serializer.save(seller=seller, category=category)
        else:
            serializer.save(seller=seller)

    def perform_update(self, serializer):
        obj = self.get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or (getattr(user, "role", None)=="seller" and obj.seller_id==user.id):
            return serializer.save()
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Not allowed.")