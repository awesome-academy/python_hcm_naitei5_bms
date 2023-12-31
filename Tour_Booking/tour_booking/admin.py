# admin.py
import xlwt
from django.contrib import admin
from .models import Tour, Booking, Image, Rating
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.translation import gettext
from datetime import datetime

class ImageInline(admin.TabularInline):
    model = Image

class TourAmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'start_date','end_date','location','created_at' )
    search_fields = ('name',)
    filter = ('start_date','end_date','location','created_at')
    inlines = [ImageInline]
    change_list_template = "admin/import_file_tour.html"

admin.site.register(Tour, TourAmin)


class BookingAmin(admin.ModelAdmin):
    list_display = ( 'status', 'created_at', 'departure_date')
    list_filter = ('status', 'created_at', 'departure_date')
    readonly_fields = ('tour', 'user', 'created_at', 'departure_date','price','end_date','number_of_people')
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        for booking in queryset:
            if booking.status == 'Pending':
                booking.status = 'Confirmed'
                booking.is_approved = True
                booking.save()

    approve_booking.short_description = 'Phê duyệt các đơn đặt Tour đã chọn'

    def save_model(self, request, obj, form, change):
        obj.approved_by = request.user
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if obj.tour.has_pending_booking() or obj.tour.has_future_bookings():
            raise ValidationError(
                "Không thể xóa Tour khi có đơn đặt đang chờ xử lý hoặc được xác nhận."
            )
        obj.delete()

    def delete_queryset(self, request, queryset):
        for booking in queryset:
            if booking.tour.has_pending_booking() or booking.tour.has_future_bookings():
                raise ValidationError(
                    f"Không thể xóa Tour '{booking.tour.name}' khi có đơn đặt đang chờ xử lý hoặc được xác nhận."
                )
        queryset.delete()
    @admin.action(description=gettext("Export Excel"))
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type="application/ms-excel")
        name = "BookingList" + datetime.now().strftime("%Y%m%d%H%M%s")
        response["Content-Disposition"] = f'attachment; filename="{name}.xls"'

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [
            "ID",
            "Tour",
            "User",
            "Price",
            "Number of People",
            "Departure Date",
            "End Date",
        ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        for row in queryset:
            row_num += 1
            tour_url = row.tour.name
            user_url = row.user.username
            
            for col_num in range(len(columns)):
                if columns[col_num] == "Departure Date" or columns[col_num] == "End Date":
                    time = getattr(row, columns[col_num].lower().replace(" ", "_"))
                    ws.write(row_num, col_num, time.strftime("%Y-%m-%d %H:%M"), font_style)
                elif columns[col_num] == "Tour":
                    ws.write(row_num, col_num, tour_url, font_style)
                elif columns[col_num] == "User":
                    ws.write(row_num, col_num, user_url, font_style)
                else:
                    ws.write(row_num, col_num, getattr(row, columns[col_num].lower().replace(" ", "_")), font_style)
        wb.save(response)
        return response
    actions = [approve_booking, export_as_excel]

admin.site.register(Booking, BookingAmin)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "rating",
    )

    def has_add_permission(self, request):
        # Vô hiệu hóa khả năng thêm mới người dùng trong trang quản trị
        return False
