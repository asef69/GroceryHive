from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from .models import WishlistItem
from .serializers import WishlistItemSerializer
# Create your views here.

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class=WishlistItemSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self): # type: ignore
        return WishlistItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # type: ignore
