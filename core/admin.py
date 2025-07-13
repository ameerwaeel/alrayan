from django.contrib import admin
from .models import TranslatedText
# Register your models here.
from django.contrib import admin
from .models import TranslatedText, HeroImage, HeroSection
admin.site.register(TranslatedText)
admin.site.register(HeroImage)  
admin.site.register(HeroSection)    
# @admin.register(TranslatedText)
# class TranslatedTextAdmin(admin.ModelAdmin):
#     list_display = ['language', 'title']
#     list_filter = ['language']
#     search_fields = ['title', 'description']

# @admin.register(HeroImage)
# class HeroImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'image']

# @admin.register(HeroSection)
# class HeroSectionAdmin(admin.ModelAdmin):
#     list_display = ['id']
#     filter_horizontal = ['titles']

