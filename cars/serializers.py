from rest_framework import serializers
from .models import *
from core.serializers import TranslatedTextSerializer
from django_countries.serializer_fields import CountryField as CountrySerializerField
from datetime import timedelta
from django.utils.html import strip_tags


class CarImageSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(write_only=True)
    car_translations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CarImage
        fields = ['car_name', 'car_translations', 'image', 'created_at', 'updated_at']

    def validate_car_name(self, value):
        clean_name = strip_tags(value).strip()

        cars = Car.objects.filter(
            name__title__icontains=clean_name
        ).distinct()

        if not cars.exists():
            raise serializers.ValidationError(f"لا توجد سيارة بالاسم '{value}'")
        if cars.count() > 1:
            raise serializers.ValidationError(f"تم العثور على أكثر من سيارة بنفس الاسم '{value}'، يجب أن يكون الاسم فريدًا.")
        return cars.first()

    def create(self, validated_data):
        car = validated_data.pop('car_name')
        return CarImage.objects.create(car=car, **validated_data)

    def get_car_translations(self, obj):
        translations = obj.car.name.all()
        return [
            {
                "language": t.language,
                "title": t.title,
                "description": t.description
            }
            for t in translations
        ]


class CarSerializer(serializers.ModelSerializer):
    name = serializers.ListField(write_only=True)
    images_car = serializers.SerializerMethodField()
    name_translations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = [
            'name', 'name_translations',
            'main_image', 'image_inside_360', 'image_outside_360',
            'image_open_door_360', 'model_year', 'price_per_day', 'price_per_hour',
            'seats', 'gear_type', 'fuel_type', 'zero_to_100_seconds',
            'child_safety_seat', 'images_car', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        name_data = validated_data.pop('name', [])
        car = Car.objects.create(**validated_data)
        for name in name_data:
            translated = TranslatedText.objects.create(**name)
            car.name.add(translated)
        return car

    def get_images_car(self, obj):
        return [
            {
                "image": image.image.url
            }
            for image in obj.images_car.all()
        ]

    def get_name_translations(self, obj):
        return [
            {
                "language": t.language,
                "title": t.title,
                "description": t.description
            }
            for t in obj.name.all()
        ]


class CarCategorySerializer(serializers.ModelSerializer):
    description = TranslatedTextSerializer(many=True)
    car = CarSerializer(many=True, read_only=True)
    car_names = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = CarCategory
        fields = ['name', 'description', 'car', 'car_names', 'created_at', 'updated_at']

    def validate_car_names(self, value):
        selected_cars = []
        for name in value:
            clean_name = strip_tags(name).strip()
            cars = Car.objects.filter(name__title__icontains=clean_name).distinct()
            if not cars.exists():
                raise serializers.ValidationError(f"لا توجد سيارة بالاسم '{name}'")
            if cars.count() > 1:
                raise serializers.ValidationError(f"تم العثور على أكثر من سيارة بنفس الاسم '{name}'، يجب أن يكون الاسم فريدًا.")
            selected_cars.append(cars.first())
        return selected_cars

    def create(self, validated_data):
        description_data = validated_data.pop('description', [])
        car_objects = validated_data.pop('car_names', [])
        category = CarCategory.objects.create(**validated_data)
        category.car.set(car_objects)
        for text in description_data:
            translated = TranslatedText.objects.create(**text)
            category.description.add(translated)
        return category



class BookingPersonSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()

    class Meta:
        model = BookingPerson
        fields = [
            'full_name', 'phone', 'email', 'comment',
            'country', 'age', 'created_at', 'updated_at'
        ]

class CarPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    images_car = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'name', 'main_image', 'image_inside_360', 'image_outside_360',
            'image_open_door_360', 'model_year', 'price_per_day', 'price_per_hour',
            'seats', 'gear_type', 'fuel_type', 'zero_to_100_seconds',
            'child_safety_seat', 'images_car'
        ]

    def get_name(self, obj):
        return [
            {
                "language": t.language,
                "title": t.title,
                "description": t.description
            }
            for t in obj.name.all()
        ]

    def get_images_car(self, obj):
        return [
            {"image": image.image.url}
            for image in obj.images_car.all()
        ]

class BookingPersonPublicSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()

    class Meta:
        model = BookingPerson
        fields = [
            'full_name', 'phone', 'email', 'comment',
            'country', 'age'
        ]

class CarBookingSerializer(serializers.ModelSerializer):
    car = CarPublicSerializer(read_only=True)  # ← النسخة بدون created/updated
    car_name = serializers.CharField(write_only=True)

    people = BookingPersonPublicSerializer(many=True, read_only=True)
    people_input = BookingPersonSerializer(many=True, write_only=True)

    class Meta:
        model = CarBooking
        fields = [
            'car', 'car_name', 'travel_date', 'return_date', 'flight_info',
            'hotel_info', 'meeting_point', 'trip_type', 'adults', 'children',
            'total_price', 'total_people', 'people', 'people_input',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_price', 'total_people', 'people']

    def validate(self, data):
        adults = data.get('adults', 0)
        children = data.get('children', 0)
        total = adults + children
        people_input = self.initial_data.get('people_input', [])
        
        if len(people_input) != total:
            raise serializers.ValidationError({
                'people_input': f"عدد الأشخاص يجب أن يساوي {total} (adults + children)"
            })

        return data  # ✅ ضروري جداً!

    def create(self, validated_data):
        people_data = validated_data.pop('people_input', [])
        car_name = validated_data.pop('car_name')

        # ✅ ابحث بأي لغة
        car = Car.objects.filter(name__title__icontains=car_name).first()
        if not car:
            raise serializers.ValidationError({'car_name': 'لم يتم العثور على سيارة بهذا الاسم بأي لغة.'})

        validated_data['car'] = car
        validated_data['total_people'] = validated_data['adults'] + validated_data['children']

        trip_type = validated_data.get('trip_type')
        travel_date = validated_data.get('travel_date')
        return_date = validated_data.get('return_date')

        if trip_type in ['pickup', 'dropoff']:
            total_price = car.price_per_hour * 2
        elif trip_type == 'both':
            total_price = car.price_per_hour * 4
        else:
            delta_days = (return_date - travel_date).days or 1
            total_price = car.price_per_day * delta_days

        validated_data['total_price'] = total_price

        booking = CarBooking.objects.create(**validated_data)

        for person in people_data:
            BookingPerson.objects.create(booking=booking, **person)

        return booking

