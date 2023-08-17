from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from tour_booking.models import Tour, FavoriteTour

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_active", "is_staff", "date_joined"]

class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id","name"]

class FavoriteTourSerializer(ModelSerializer):
    class Meta:
        model = FavoriteTour
        fields = ["id","name"]
