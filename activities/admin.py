from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Activity)
admin.site.register(ActivityCategory)
admin.site.register(ActivityImage)
admin.site.register(ActivityBooking)
admin.site.register(BookingPerson)
