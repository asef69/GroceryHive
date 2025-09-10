from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import ProfileSerializer
from .models import Profile
# Create your views here.

class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user.profile # type: ignore
