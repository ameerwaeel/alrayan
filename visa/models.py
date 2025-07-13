from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from core.models import TranslatedText

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

VISA_TYPES = [
    ('free', 'Visa Free'),
    ('evisa', 'E-Visa'),
    ('other', 'Other'),
]

class Country(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)  
    country = CountryField(blank=False,null=False,verbose_name="country")  # حقل الدولة الجاهز
    flag_image = models.ImageField(upload_to='flags/',blank=False,null=False,verbose_name="flag")
    visa_type = models.CharField(max_length=10, choices=VISA_TYPES,blank=False,null=False,verbose_name="type of visa")
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False,verbose_name="price")

    def __str__(self):
        return self.country.name
    
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.country)
            slug = base_slug
            counter = 1
            while Country.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        if not self.pk or Country.objects.get(pk=self.pk).country != self.country:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Country")
        verbose_name_plural = ("Countries")


class VisaCard(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    name=models.CharField(max_length=100,blank=False,null=False,verbose_name="type of visa")
    country = models.ForeignKey(Country, on_delete=models.CASCADE,blank=False,null=False,verbose_name="country")
    image = models.ImageField(upload_to='visa_cards/',blank=False,null=False,verbose_name="image")
    text = models.ManyToManyField('core.TranslatedText', related_name='visa_titles',verbose_name="languages")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while VisaCard.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        if not self.pk or VisaCard.objects.get(pk=self.pk).name != self.name:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("visa card")
        verbose_name_plural = ("visa cards")  


class VisaSection(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,verbose_name="type of visa")
    slug = models.SlugField(unique=True, blank=True,verbose_name="type of visa")      
    section_name = models.CharField(max_length=100,blank=False,null=False,verbose_name="name of section")  # free / evisa / other
    text = models.ManyToManyField('core.TranslatedText', related_name='section_titles',verbose_name="languages")
    cards = models.ManyToManyField(VisaCard, related_name='visa_sections',verbose_name="which card")

    def __str__(self):
        return self.section_name
    
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(self.section_name)
            slug = base_slug
            counter = 1
            while VisaSection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        if not self.pk or VisaSection.objects.get(pk=self.pk).section_name != self.section_name:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("visa section")
        verbose_name_plural = ("visa sections") 


class Booking(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    travel_date = models.DateField(verbose_name="date of travel")
    return_date = models.DateField(verbose_name="date of return")
    flight_info = CKEditor5Field( config_name='default',verbose_name="info of flight")
    hotel_info = CKEditor5Field( config_name='default',verbose_name="info of hotels")
    adults = models.PositiveIntegerField(blank=False,null=False,verbose_name="adults")
    children = models.PositiveIntegerField(blank=False,null=False,verbose_name="children")
    total_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="total price")
    total_people = models.PositiveIntegerField(verbose_name="total people")

    def __str__(self):
        return self.travel_date
    
    def save(self, *args, **kwargs):
        def generate_unique_slug():
            base_slug = slugify(f"{self.travel_date}-{self.return_date}")
            slug = base_slug
            counter = 1
            while Booking.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        calculated_people = self.adults + self.children
        if self.total_people != calculated_people:
            raise ValueError("عدد الأشخاص لا يساوي عدد البالغين + الأطفال.")
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Booking")
        verbose_name_plural = ("Bookings") 

class BookingPerson(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)      
    booking = models.ForeignKey(Booking, related_name='people', on_delete=models.CASCADE,verbose_name="which booking")
    full_name = models.CharField(max_length=255,blank=False,null=False,verbose_name="full name")
    phone = models.CharField(max_length=20,blank=False,null=False,verbose_name="phone")
    email = models.EmailField(blank=False,null=False,verbose_name="email")
    image = models.ImageField(upload_to='person_images/',blank=True, null=True,verbose_name="image of person")
    address = models.TextField(blank=False,null=False,verbose_name="address of person")
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False,verbose_name="nationality")
    visa_image = models.ImageField(upload_to='visa_docs/',blank=True, null=True,verbose_name="image of visa")
    age = models.PositiveIntegerField(blank=False,null=False,verbose_name="age")

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
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Booking person")
        verbose_name_plural = ("Booking persons") 


    




