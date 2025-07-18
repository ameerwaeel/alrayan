from rest_framework import serializers
from .models import *
import re 
from rest_framework import serializers
from .models import Find_Us, Get_In_Touch
from core.models import TranslatedText


class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactForm
        fields = ['full_name', 'email', 'phone', 'country', 'message','created_at','updated_at' ]
        extra_kwargs = {
            'full_name':    {'required': True, 'allow_null': False, 'allow_blank': False},
            'email':  {'required': True, 'allow_null': False, 'allow_blank': False},
            'phone':   {'required': True, 'allow_null': False},
            'country': {'required': True, 'allow_null': False, 'allow_blank': False},
            'message':    {'required': False, 'allow_null': True, 'allow_blank': True},
        }

    def validate(self, attrs):
        errors = {}

        for field in ['full_name', 'email', 'phone', 'country']:
            value = attrs.get(field)

            if value is None:
                errors[field] = f"The {field} field is required and cannot be left blank or empty."
                continue

            if isinstance(value, str):
                if not value.strip():
                    errors[field] = f"The {field} field cannot be empty."
                elif field in ['full_name'] and len(value.strip()) < 3:
                    errors[field] = f"The {field} must contain at least 3 characters."

            if field == 'email':
                email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                if not re.match(email_regex, value):
                    errors[field] = "Please enter a valid email address."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

class NewsletterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = Newsletter
        fields = ['email','created_at','updated_at']
    def validate(self, data):
        email = data.get('email')

        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        if Newsletter.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already subscribed."})

        return data





class TranslatedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedText
        fields = ['title', 'description', 'language']

class FindUsSerializer(serializers.ModelSerializer):
    description = TranslatedTextSerializer(many=True)

    class Meta:
        model = Find_Us
        fields = ['description', 'link_location', 'location_name','created_at','updated_at']

    def create(self, validated_data):
        descriptions_data = self.initial_data.get('description', [])
        find_us = Find_Us.objects.create(
            link_location=validated_data.get('link_location'),
            location_name=validated_data.get('location_name')
        )
        for desc in descriptions_data:
            translated = TranslatedText.objects.create(**desc)
            find_us.description.add(translated)
        return find_us
    
# class GetInTouchSerializer(serializers.ModelSerializer):
#     get_in_touch = TranslatedTextSerializer(many=True, read_only=True)

#     class Meta:
#         model = Get_In_Touch
#         fields = ['description','created_at','updated_at']    
#     def create(self, validated_data):
#         description_data = validated_data.pop('description')
#         get_in_touch_instance = Get_In_Touch.objects.create(**validated_data)

#         for desc in description_data:
#             translated = TranslatedText.objects.create(**desc)
#             get_in_touch_instance.description.add(translated)

#         return get_in_touch_instance        
class GetInTouchSerializer(serializers.ModelSerializer):
    description = TranslatedTextSerializer(many=True)

    class Meta:
        model = Get_In_Touch
        fields = ['description','created_at','updated_at']

    def create(self, validated_data):
        descriptions_data = validated_data.pop('description')
        get_in_touch_instance = Get_In_Touch.objects.create()
        for desc_data in descriptions_data:
            translated_text = TranslatedText.objects.create(**desc_data)
            get_in_touch_instance.description.add(translated_text)
        return get_in_touch_instance