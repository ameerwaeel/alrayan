

from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.prefetch_related('name', 'images_car').all()
    serializer_class = CarSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.prefetch_related('name', 'images_car').all()
    serializer_class = CarSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarImageListCreateView(generics.ListCreateAPIView):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarCategoryListCreateView(generics.ListCreateAPIView):
    queryset = CarCategory.objects.prefetch_related('description').all()
    serializer_class = CarCategorySerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarCategory.objects.prefetch_related('description').all()
    serializer_class = CarCategorySerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarBookingListCreateView(generics.ListCreateAPIView):
    queryset = CarBooking.objects.prefetch_related('people', 'car').all()
    serializer_class = CarBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBooking.objects.prefetch_related('people', 'car').all()
    serializer_class = CarBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
