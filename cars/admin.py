from django.contrib import admin

# Register your models here.
from .models import *
# admin.site.register(CarCategory)
admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(CarBooking)
admin.site.register(BookingPerson)  
@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)  # ✅ أخفي السلاج من الفورم    
# @admin.register(CarCategory)
# class CarCategoryAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']  # للبحث بالاسم

# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ['get_name', 'category', 'model_year', 'price_per_day', 'gear_type', 'fuel_type']
#     list_filter = ['category', 'gear_type', 'fuel_type', 'model_year']
#     search_fields = ['id']

#     def get_name(self, obj):
#         return obj.name.first().title if obj.name.exists() else '-'
#     get_name.short_description = 'Car Name'

# @admin.register(CarImage)
# class CarImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'image']

# @admin.register(CarBooking)
# class CarBookingAdmin(admin.ModelAdmin):
#     list_display = ['car', 'travel_date', 'return_date', 'trip_type', 'adults', 'children', 'total_price']
#     list_filter = ['trip_type', 'travel_date']
#     search_fields = ['car__id', 'car__name__title']

# @admin.register(BookingPerson)
# class BookingPersonAdmin(admin.ModelAdmin):
#     list_display = ['full_name', 'phone', 'email', 'country']
#     search_fields = ['full_name', 'email']

