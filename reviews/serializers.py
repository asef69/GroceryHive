from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id","product","rating","comment","created_at")
        read_only_fields = ("created_at",)

    def validate_rating(self, v):
        if not 1 <= v <= 5:
            raise serializers.ValidationError("Rating must be between 1 to 5")
        return v