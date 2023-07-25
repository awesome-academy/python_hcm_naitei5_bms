# admin.py
from django.contrib import admin
from .models import Tour, Booking, Image, Rating

class ImageInline(admin.TabularInline):
    model = Image

class TourAmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date')
    search_fields = ('name',)
    list_filter = ('date',)
    inlines = [ImageInline]

admin.site.register(Tour, TourAmin)


class BookingAmin(admin.ModelAdmin):
    list_display = ( 'status', 'created_at', 'departure_date')
    list_filter = ('status', 'created_at', 'departure_date')

admin.site.register(Booking, BookingAmin)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "rating",
    )

    def has_add_permission(self, request):
        # Vô hiệu hóa khả năng thêm mới người dùng trong trang quản trị
        return False
