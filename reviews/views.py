from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: return True
        return obj.user_id == request.user.id

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("product","user")
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        product_pk = self.kwargs.get("product_pk")
        if product_pk:
            qs = qs.filter(product_id=product_pk)
        return qs

    def perform_create(self, serializer):
        product_pk = self.kwargs.get("product_pk")
        if product_pk:
            serializer.save(user=self.request.user, product_id=product_pk)
        else:
            serializer.save(user=self.request.user)