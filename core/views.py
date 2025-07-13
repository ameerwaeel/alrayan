from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django_countries import countries
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import *
from .serializers import *



class TranslatedTextListCreateView(generics.ListCreateAPIView):
    queryset = TranslatedText.objects.all()
    serializer_class = TranslatedTextSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class TranslatedTextDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TranslatedText.objects.all()
    serializer_class = TranslatedTextSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    # lookup_field = 'uuid'    
from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import HeroSection
from .serializers import HeroSectionSerializer

class HeroSectionListCreateView(generics.ListCreateAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
class HeroSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HeroSection
from .serializers import HeroSectionSerializer

class HeroSectionView(APIView):
    def get(self, request):
        page = request.query_params.get('page', 'homepage')
        hero = HeroSection.objects.filter(page=page).first()
        if not hero:
            return Response({"detail": "Not found."}, status=404)
        return Response(HeroSectionSerializer(hero).data)
