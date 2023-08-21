from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from tour_booking.models import Tour, FavoriteTour, Booking, Rating, Reply
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

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["user","tour","rating","content"]

class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ["user","content","parent_comment"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["user","tour","number_of_people","price","departure_date","end_date"]

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

class RevenueStatisticsSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    tour_name = serializers.CharField(source='tour.name')

    fields = ["total_revenue", "tour_name"]

class BookingRatioStatisticsSerializer(serializers.Serializer):
    total_booking = serializers.IntegerField()
    tour_details = TourSerializer(many=True)

    def get_tour_details(self, obj):
        tour_details = []
        for tour in obj['tour_details']:
            booking_count = Booking.objects.filter(tour=tour).count()
            tour_details.append({
                "tour": TourSerializer(tour).data,
                "booking_count": booking_count
            })
        return tour_details

class MonthlyRevenueSerializer(serializers.Serializer):
    tour_name = serializers.CharField()
    monthly_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_bookings = serializers.IntegerField()
