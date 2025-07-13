from rest_framework import serializers
from .models import *
import json


class TranslatedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedText
        fields = [ 'language', 'title', 'description']


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = [ 'image']


# class HeroSectionSerializer(serializers.ModelSerializer):
#     images = HeroImageSerializer(many=True, read_only=True)
#     texts = TranslatedTextSerializer(many=True, read_only=True)

#     class Meta:
#         model = HeroSection
#         fields = ['page', 'images', 'texts']

class HeroSectionSerializer(serializers.ModelSerializer):
    texts = TranslatedTextSerializer(many=True)
    images = HeroImageSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = HeroSection
        fields = ['updated_at', 'created_at', 'page', 'texts', 'images']

    # def create(self, validated_data):
    #     texts_data = validated_data.pop('texts', [])
    #     images_data = self.context['request'].FILES.getlist('images')

    #     hero_section = HeroSection.objects.create(page=validated_data.get('page'))

    #     for text_data in texts_data:
    #         text_instance = TranslatedText.objects.create(**text_data)
    #         hero_section.texts.add(text_instance)

    #     for image in images_data:
    #         HeroImage.objects.create(hero_section=hero_section, image=image)

    #     return hero_section

    def create(self, validated_data):
        request = self.context.get('request')

        # نحصل على النصوص الخام من request.data (وليس من validated_data)
        texts_raw = request.data.get('texts')
        texts_data = json.loads(texts_raw) if texts_raw else []

        images = request.FILES.getlist('images')
        hero_section = HeroSection.objects.create(page=validated_data.get('page'))

        for text in texts_data:
            trans = TranslatedText.objects.create(**text)
            hero_section.texts.add(trans)

        for image in images:
            HeroImage.objects.create(hero_section=hero_section, image=image)

        return hero_section
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['texts'] = TranslatedTextSerializer(instance.texts.all(), many=True).data
        rep['images'] = HeroImageSerializer(instance.images.all(), many=True).data
        return rep
