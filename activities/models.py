from django.db import models
from django.utils.text import slugify
import uuid
from core.models import TranslatedText
from django_countries.fields import CountryField
from django_ckeditor_5.fields import CKEditor5Field

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Activity(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    main_image = models.ImageField(upload_to='activities/main/')
    video_link = models.URLField(blank=True, null=True)
    image_of_video = models.ImageField(upload_to='activities/video_img/')
    name = CKEditor5Field('name', config_name='default')
    days = models.PositiveIntegerField()
    nights = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location_name = models.CharField(max_length=255)
    location_link = models.URLField()
    stars = models.PositiveIntegerField()
    reviews = models.PositiveIntegerField()
    love = models.PositiveIntegerField()
    details = CKEditor5Field('details', config_name='default')
    overviews = CKEditor5Field('overviews', config_name='default')    
    ages = models.CharField(max_length=50)
    max_groups = models.PositiveIntegerField()
    duration = models.DurationField()
    start_time = models.TimeField()
    included = models.CharField(max_length=255)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.location_name)
            slug = base_slug
            counter = 1
            while Activity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ActivityCategory(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    activities = models.ManyToManyField(Activity, related_name='categories')
    text = models.ManyToManyField(TranslatedText, related_name='activity_category_texts')

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = "activity-category"
            slug = base_slug
            counter = 1
            while ActivityCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ActivityImage(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='activities/gallery/')

    def __str__(self):
        return f"{self.activity} image"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(str(self.img))
            slug = base_slug
            counter = 1
            while ActivityImage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ActivityBooking(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    datebooking = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_people = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return f"Booking for {self.activity}"

    def save(self, *args, **kwargs):
        self.total_people = self.adults + self.children
        self.total_price = self.activity.price * self.total_people
        if not self.slug:
            base_slug = slugify(str(self.activity))
            slug = base_slug
            counter = 1
            while ActivityBooking.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class BookingPerson(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    booking = models.ForeignKey(ActivityBooking, on_delete=models.CASCADE, related_name='people')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    number = models.CharField(max_length=20)
    country = CountryField()
    comment = CKEditor5Field('comment', config_name='default')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while BookingPerson.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
