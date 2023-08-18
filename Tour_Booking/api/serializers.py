from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from tour_booking.models import Tour, FavoriteTour
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_active", "is_staff", "date_joined", "last_name","first_name",]

class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id","name"]

class FavoriteTourSerializer(ModelSerializer):
    class Meta:
        model = FavoriteTour
        fields = ["id","name"]

class ChangeUserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
