from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from core.models import TranslatedText
from django_countries.fields import CountryField
from django_ckeditor_5.fields import CKEditor5Field

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

TRIP_TYPES = [
    ('pickup', 'استقبال مطار'),
    ('dropoff', 'توديع مطار'),
    ('both', 'استقبال وتوديع'),
    ('all', 'الكل'),
]

FUEL_TYPES = [
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('electric', 'Electric'),
]

GEAR_TYPES = [
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
]


class CarImage(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='images_car',verbose_name="car")
    image = models.ImageField(upload_to='cars/gallery/',null=False, blank=False,verbose_name="image of cars")

    def __str__(self):
        return f"Image for {self.car}"

    def save(self, *args, **kwargs): 
        def generate_unique_slug():
            base_slug = slugify(self.image)
            slug = base_slug
            counter = 1
            while CarImage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.pk or CarImage.objects.get(pk=self.pk).image != self.image:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Car Image"
        verbose_name_plural = "Car Images"    
# ---- كاتيجوري ----
class CarCategory(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    name = models.CharField(max_length=255,verbose_name="category name")
    description = models.ManyToManyField('core.TranslatedText', related_name='car_category_descs',verbose_name="category description")
    car = models.ManyToManyField('Car', related_name='category_cars',verbose_name="category car")

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while CarCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.slug:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Car category"
        verbose_name_plural = "Car categories"   
# ---- السيارة ----
class Car(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    name = models.ManyToManyField('core.TranslatedText', related_name='car_names',verbose_name="car")
    main_image = models.ImageField(upload_to='cars/main/',null=False, blank=False,verbose_name="main img of car")
    image_inside_360 = models.ImageField(upload_to='cars/inside360/',null=False, blank=False,verbose_name="inside img of car")
    image_outside_360 = models.ImageField(upload_to='cars/outside360/',null=False, blank=False,verbose_name="outside img of car")
    image_open_door_360 = models.ImageField(upload_to='cars/door360/', null=False, blank=False,verbose_name="open door img of car")
    model_year = models.PositiveIntegerField(verbose_name="year of model")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="price per day")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="price per hour")
    seats = models.PositiveIntegerField(verbose_name="seats")
    gear_type = models.CharField(max_length=10, choices=GEAR_TYPES,verbose_name="type of gear")
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES,verbose_name="type of fuel")
    zero_to_100_seconds = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="zero to 100 seconds")
    child_safety_seat = models.BooleanField(default=False,verbose_name="child safety seat")

    def __str__(self):
        first_translation = self.name.first()
        if first_translation:
            return str(first_translation.title)
        return "Unnamed Car"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # احفظ الأول عشان نقدر نستخدم name
        if not self.slug:
            first_name = self.name.first()
            base_text = first_name.title if first_name else f"car-{self.pk}"
            base_slug = slugify(base_text)
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            super().save(update_fields=["slug"])
    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"     
  
# ---- الحجز ----
class CarBooking(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    car = models.ForeignKey(Car, on_delete=models.CASCADE,verbose_name="car")
    travel_date = models.DateField(verbose_name="date of travel")
    return_date = models.DateField(verbose_name="date of return")
    flight_info = models.TextField(verbose_name="flight info")
    hotel_info = models.TextField(verbose_name="hotel info")
    meeting_point = models.CharField(max_length=255,verbose_name="meeting point")
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPES,verbose_name="type of trip")
    adults = models.PositiveIntegerField(verbose_name="adults")
    children = models.PositiveIntegerField(verbose_name="children")
    total_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="total price")
    total_people = models.PositiveIntegerField(verbose_name="total people")

    def __str__(self):
        return f"Booking for {self.car}"
    
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(str(self.car))
            slug = base_slug
            counter = 1
            while CarBooking.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        # احسب عدد الأشخاص
        calculated_people = self.adults + self.children
        self.total_people = calculated_people

        # احسب السعر الإجمالي بناءً على نوع الرحلة
        if self.trip_type in ['pickup', 'dropoff']:
            self.total_price = self.car.price_per_hour * 2
        elif self.trip_type == 'both':
            self.total_price = self.car.price_per_hour * 4
        else:
            # احسب عدد الأيام بدقة
            delta_days = (self.return_date - self.travel_date).days or 1
            self.total_price = self.car.price_per_day * delta_days

        # توليد slug إذا مش موجود أو السيارة اتغيّرت
        if not self.pk or not CarBooking.objects.filter(pk=self.pk).exists() or CarBooking.objects.get(pk=self.pk).car != self.car:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Car Booking"
        verbose_name_plural = "Car Bookings" 

# ---- الأشخاص داخل الحجز ----
class BookingPerson(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    booking = models.ForeignKey(CarBooking, related_name='people', on_delete=models.CASCADE,verbose_name="booking")
    full_name = models.CharField(max_length=255,verbose_name="full name")
    phone = models.CharField(max_length=20,verbose_name="phone")
    email = models.EmailField(verbose_name="email")
    comment = CKEditor5Field( config_name='default',verbose_name="comment")
    country = CountryField(verbose_name="country")
    age = models.PositiveIntegerField(verbose_name="age")

    def __str__(self):
        return self.full_name
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while BookingPerson.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug

        if not self.pk or BookingPerson.objects.get(pk=self.pk).full_name != self.full_name:
            self.slug = generate_unique_slug()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Booking Person"
        verbose_name_plural = "Booking Persons"     