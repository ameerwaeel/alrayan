from rest_framework import serializers
from .models import *
from core.serializers import TranslatedTextSerializer
from django_countries.serializer_fields import CountryField as CountrySerializerField

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = ['img','activity','created_at', 'updated_at']

class ActivitySerializer(serializers.ModelSerializer):
    images = ActivityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['main_image', 'video_link', 'image_of_video', 
                'name', 'days', 'nights','price', 'location_name',
                'location_link','stars', 'reviews', 'love', 'details',
                'overviews', 'ages', 'max_groups', 'duration',
                'start_time', 'included', 'created_at', 'updated_at']

class ActivityCategorySerializer(serializers.ModelSerializer):
    text = TranslatedTextSerializer(many=True)
    activities = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), many=True)

    class Meta:
        model = ActivityCategory
        fields = ['text','activities','created_at', 'updated_at']

# class BookingPersonSerializer(serializers.ModelSerializer):
#     country = CountrySerializerField()

#     class Meta:
#         model = BookingPerson
#         exclude = ['booking']

class BookingPersonSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()

    class Meta:
        model = BookingPerson
        fields = [
            'full_name', 'phone', 'email', 'comment',
            'country', 'age', 'created_at', 'updated_at'
        ]

class ActivityBookingSerializer(serializers.ModelSerializer):
    people = BookingPersonSerializer(many=True, read_only=True)
    people_input = BookingPersonSerializer(many=True, write_only=True)

    class Meta:
        model = ActivityBooking
        fields = [
            'activity', 'adults', 'children', 'datebooking',
            'total_price', 'total_people', 'people', 'people_input'
        ]
        read_only_fields = ['total_price', 'total_people', 'people', 'created_at', 'updated_at']

    def validate(self, data):
        total = data.get('adults', 0) + data.get('children', 0)
        people_input = self.initial_data.get('people_input', [])
        if len(people_input) != total:
            raise serializers.ValidationError("عدد الأشخاص لا يساوي البالغين + الأطفال")
        return data

    def create(self, validated_data):
        people_data = validated_data.pop('people_input')
        booking = ActivityBooking.objects.create(**validated_data)
        for person in people_data:
            BookingPerson.objects.create(booking=booking, activity=booking.activity, **person)
        return booking
