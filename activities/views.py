from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

class ActivityCategoryListCreateView(generics.ListCreateAPIView):
    queryset = ActivityCategory.objects.prefetch_related('text')
    serializer_class = ActivityCategorySerializer

class ActivityImageListCreateView(generics.ListCreateAPIView):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

class ActivityBookingListCreateView(generics.ListCreateAPIView):
    queryset = ActivityBooking.objects.prefetch_related('people')
    serializer_class = ActivityBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
