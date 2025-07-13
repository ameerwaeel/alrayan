from rest_framework import serializers
from .models import *
from django_countries.serializer_fields import CountryField as CountrySerializerField
from core.serializers import TranslatedTextSerializer
from django_countries.serializer_fields import CountryField as CountrySerializerField
from core.models import TranslatedText
from rest_framework import serializers
# from core.serializers import CountrySerializer
from .models import Booking, BookingPerson
from django_countries.fields import CountryField


 
class CountrySerializer(serializers.ModelSerializer):
    country = CountrySerializerField()
    class Meta:
        model = Country
        fields = [ 'updated_at','created_at',  'country', 'flag_image', 'visa_type', 'price', ]


class CountryPublicSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()

    class Meta:
        model = Country
        fields = ['country', 'flag_image', 'visa_type', 'price']

class VisaCardSerializer(serializers.ModelSerializer):
    text = TranslatedTextSerializer(many=True)
    country = CountrySerializer(read_only=True)
    country_id = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        slug_field='country',
        write_only=True,
        source='country'
    )

    class Meta:
        model = VisaCard
        fields = [
            'updated_at', 'created_at', 'name', 'image',
            'text', 'country', 'country_id'
        ]

    def create(self, validated_data):
        text_data = validated_data.pop("text", [])
        visa_card = VisaCard.objects.create(**validated_data)

        for text in text_data:
            translated = TranslatedText.objects.create(**text)
            visa_card.text.add(translated)

        return visa_card



class VisaSectionSerializer(serializers.ModelSerializer):
    text = TranslatedTextSerializer(many=True, read_only=True)
    text_data = TranslatedTextSerializer(many=True, write_only=True)
    
    cards = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=VisaCard.objects.all(),
        write_only=True
    )
    cards_details = VisaCardSerializer(source='cards', many=True, read_only=True)

    class Meta:
        model = VisaSection
        fields = ['section_name', 'text', 'text_data', 'cards', 'cards_details']

    def create(self, validated_data):
        text_data = validated_data.pop('text_data', [])
        cards_data = validated_data.pop('cards', [])

        section = VisaSection.objects.create(**validated_data)

        for text in text_data:
            translated = TranslatedText.objects.create(**text)
            section.text.add(translated)

        section.cards.set(cards_data)

        return section




class BookingPersonSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    visa_image = serializers.ImageField(required=False, allow_null=True)

    # input فقط
    nationality_id = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        slug_field='country',
        write_only=True,
        source='nationality'
    )

    # output فقط (بدون uuid, created_at, updated_at)
    nationality = CountryPublicSerializer(read_only=True)

    class Meta:
        model = BookingPerson
        fields = [
            'full_name', 'phone', 'email',
            'image', 'address', 'nationality_id',
            'nationality', 'visa_image', 'age',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    people = BookingPersonSerializer(many=True, read_only=True)
    people_input = BookingPersonSerializer(many=True, write_only=True)

    class Meta:
        model = Booking
        fields = [
            'created_at', 'updated_at',
            'travel_date', 'return_date',
            'flight_info', 'hotel_info',
            'adults', 'children', 'total_price', 'total_people',
            'people', 'people_input'
        ]
        read_only_fields = [
            'created_at', 'updated_at',
            'total_price', 'total_people', 'people'
        ]

    def validate(self, data):
        adults = data.get('adults', 0)
        children = data.get('children', 0)
        total_people = adults + children
        people_list = self.initial_data.get('people_input', [])

        if len(people_list) != total_people:
            raise serializers.ValidationError({
                'people_input': f"عدد الأشخاص يجب أن يكون = {total_people} (adults + children)"
            })

        return data

    def create(self, validated_data):
        people_data = validated_data.pop('people_input', [])
        total_people = validated_data.get('adults', 0) + validated_data.get('children', 0)
        validated_data['total_people'] = total_people

        total_price = 0
        for person in people_data:
            nationality = person['nationality']
            total_price += nationality.price

        validated_data['total_price'] = total_price

        booking = Booking.objects.create(**validated_data)

        for person_data in people_data:
            BookingPerson.objects.create(booking=booking, **person_data)

        return booking