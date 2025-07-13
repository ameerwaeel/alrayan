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

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    # queryset = Booking.objects.prefetch_related('people').select_related('country').all()
    queryset = Booking.objects.prefetch_related('people').all()
    serializer_class = BookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # booking = Booking.objects.prefetch_related('people', 'country').get(pk=booking.pk)
        booking = Booking.objects.prefetch_related('people').get(pk=booking.pk)

        return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Booking.objects.prefetch_related('people').select_related('country').all()
    queryset = Booking.objects.prefetch_related('people').all()
    serializer_class = BookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

  

class VisaSectionListCreateView(generics.ListCreateAPIView):
    queryset = VisaSection.objects.all()
    serializer_class = VisaSectionSerializer 
    parser_classes = [JSONParser,MultiPartParser, FormParser]

class VisaSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VisaSection.objects.all()
    serializer_class = VisaSectionSerializer
    parser_classes = [JSONParser,MultiPartParser, FormParser]
    lookup_field = 'uuid'    

class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'    




class CountryListView(APIView):
    def get(self, request):
        country_list = [{"code": code, "name": name} for code, name in countries]
        total_countries = len(country_list)
        return Response({
            "total": total_countries,
            "countries": country_list
        })
    


  
class VisaCardListCreateView(generics.ListCreateAPIView):
    serializer_class = VisaCardSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return VisaCard.objects.select_related('country').prefetch_related('text')


class VisaCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VisaCardSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

    def get_queryset(self):
        return VisaCard.objects.select_related('country').prefetch_related('text')

