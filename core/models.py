from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils import timezone
import uuid

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('ru', 'Russian'),
]

class TranslatedText(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    language = models.CharField(max_length=2, choices=LANGUAGES)
    title = CKEditor5Field('title', config_name='default')
    description = CKEditor5Field('Description', config_name='default')
    def __str__(self):
        return f"{self.language} - {self.title} - {self.description}"
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TranslatedText.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.pk or TranslatedText.objects.get(pk=self.pk).title != self.title:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)
    
class HeroSection(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    page = models.CharField(max_length=100)
    texts = models.ManyToManyField('TranslatedText', related_name='hero_sections')
    
    def __str__(self):
        return self.page
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.page)
            slug = base_slug
            counter = 1
            while HeroSection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.pk or HeroSection.objects.get(pk=self.pk).page != self.page:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)    
def upload_to(instance, filename):
    return f"hero_section/{instance.hero_section.page}/{filename}"

class HeroImage(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    hero_section = models.ForeignKey(HeroSection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f"{self.hero_section.page} - image"
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.image)
            slug = base_slug
            counter = 1
            while HeroImage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.pk or HeroImage.objects.get(pk=self.pk).image != self.image:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)    
# class HeroImage(models.Model):
#     image = models.ImageField(upload_to='hero_images/')

#     def __str__(self):
#         return f"Image for {self.image}"
    
# class HeroSection(models.Model):
#     titles = models.ManyToManyField(TranslatedText, related_name='hero_titles')
#     image = models.ForeignKey(HeroImage, on_delete=models.CASCADE, related_name='images')

#     def __str__(self):
#         return f"Hero for {self.titles}"


# class Page(models.Model):
#     name = models.CharField(max_length=100)    
#     HeroSection = models.OneToOneField(HeroSection, on_delete=models.CASCADE, related_name='hero_section')
     
#     def __str__(self):
#         return self.name
    