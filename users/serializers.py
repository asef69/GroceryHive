from rest_framework import serializers
from .models import User,Profile

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','password','role']
        extra_kwargs={'password':{'write_only':True}}



class ProfileSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(source='user.email',read_only=True)
    role=serializers.CharField(source='user.role',read_only=True)
    class Meta:
        model=Profile
        fields=['email','role','contact_phone','preferences']