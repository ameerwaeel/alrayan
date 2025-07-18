from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from core.models import TranslatedText
from django_countries.fields import CountryField
from django_ckeditor_5.fields import CKEditor5Field

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('ru', 'Russian'),
]

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ContactForm(TimeStampedModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)    
    full_name = models.CharField(max_length=255, null=False ,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=False ,blank=False)
    country = CountryField(verbose_name="country")
    message = models.TextField()

    def __str__(self):
        return str(self.full_name)  
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = ContactForm.objects.get(pk=self.pk)
            if old.full_name != self.full_name:
                # الاسم اتغير، نولّد سلاج جديد
                base_slug = slugify(self.full_name)
                slug = base_slug
                counter = 1
                while ContactForm.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
        else:
            # تسجيل جديد
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while ContactForm.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)    
         

class Newsletter(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    email = models.EmailField(unique=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.email)
        super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.pk:
            old = Newsletter.objects.get(pk=self.pk)
            if old.email != self.email:
                # الاسم اتغير، نولّد سلاج جديد
                base_slug = slugify(self.email)
                slug = base_slug
                counter = 1
                while Newsletter.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
        else:
            # تسجيل جديد
            base_slug = slugify(self.email)
            slug = base_slug
            counter = 1
            while Newsletter.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs) 

class Find_Us(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)       
    description = models.ManyToManyField(
        'core.TranslatedText',
        verbose_name="description",
        related_name='find_us_descriptions'
    )
    link_location = models.URLField(blank=True, null=True, verbose_name="link of location")
    location_name = CKEditor5Field(config_name='default', verbose_name="location_name")

    class Meta:
        verbose_name = ("Find_Us")
        verbose_name_plural = ("Find_Us")

    def __str__(self):
        first_translation = self.description.first()
        return str(first_translation.title) if first_translation else "Unnamed"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(str(self.uuid))
            slug = base_slug
            counter = 1
            while Find_Us.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Get_In_Touch(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)       
    description = models.ManyToManyField(
        'core.TranslatedText',
        related_name='get_in_touch_descriptions',  # ✅ تم التعديل هنا
        verbose_name="description"
    )

    class Meta:
        verbose_name = ("Get_In_Touch")
        verbose_name_plural = ("Get_In_Touch")

    def __str__(self):
        first_translation = self.description.first()
        return str(first_translation.title) if first_translation else "Unnamed"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(str(self.uuid))
            slug = base_slug
            counter = 1
            while Get_In_Touch.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

# class Find_Us(TimeStampedModel):
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     slug = models.SlugField(unique=True, blank=True)       
#     description=models.ManyToManyField(
#         'core.TranslatedText',
#         verbose_name="description",
#         related_name='find_us_descriptions'  # وهذا كمان
#     )
#     link_location=models.URLField(blank=True, null=True,verbose_name="link of location")
#     location_name=CKEditor5Field( config_name='default',verbose_name="location_name")
#     class Meta:
#         verbose_name = ("Find_Us")
#         verbose_name_plural = ("Find_Us")

#     def __str__(self):
#         first_translation = self.description.first()
#         if first_translation:
#             return str(first_translation.title)
#         return "Unnamed"
    
# class Get_In_Touch(TimeStampedModel):
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     slug = models.SlugField(unique=True, blank=True)       
#     description = models.ManyToManyField(
#         'core.TranslatedText',
#         related_name='find_us_descriptions',  # ✅ بدون تكرار
#         verbose_name="description"
#     )
#     class Meta:
#         verbose_name = ("Get_In_Touch")
#         verbose_name_plural = ("Get_In_Touch")

#     def __str__(self):
#         first_translation = self.description.first()
#         if first_translation:
#             return str(first_translation.title)
#         return "Unnamed"
