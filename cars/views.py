

from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import *
from .serializers import *
from django.core.mail import EmailMessage
import threading
import logging

from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def send_booking_email(subject, body, from_email):
    def send_email():
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=["mrseller.prof@gmail.com"],
            )
            email.send()
        except Exception as e:
            logger.error(f"Failed to send booking email: {e}")
    threading.Thread(target=send_email).start()

class CarBookingListCreateView(generics.ListCreateAPIView):
    queryset = CarBooking.objects.prefetch_related('people', 'car').all()
    serializer_class = CarBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # إعادة جلب الحجز مع علاقاته
        booking = CarBooking.objects.prefetch_related('people').get(pk=booking.pk)

        subject = f"Car Booking - {booking.car} on {booking.travel_date}"
        body = f"""
تم إنشاء حجز سيارة جديد:

• السيارة: {booking.car}
• نوع الرحلة: {booking.trip_type}
• نقطة اللقاء: {booking.meeting_point}
• تاريخ السفر: {booking.travel_date}
• تاريخ العودة: {booking.return_date}
• عدد البالغين: {booking.adults}
• عدد الأطفال: {booking.children}
• عدد الأشخاص: {booking.total_people}
• السعر الإجمالي: {booking.total_price} 

• تفاصيل الرحلة: {booking.flight_info}
• تفاصيل الفندق: {booking.hotel_info}

المسافرون:
"""

        for person in booking.people.all():
            body += f"""
    - الاسم: {person.full_name}
      البريد: {person.email}
      الجنسية: {person.country}
      العمر: {person.age}
      الهاتف: {person.phone}
      التعليق: {person.comment}
      تاريخ الإضافة: {person.created_at}
      آخر تحديث: {person.updated_at}
"""

        from_email = booking.people.first().email if booking.people.exists() else "noreply@example.com"
        send_booking_email(subject, body, from_email)

        return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)

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


# class CarBookingListCreateView(generics.ListCreateAPIView):
#     queryset = CarBooking.objects.prefetch_related('people', 'car').all()
#     serializer_class = CarBookingSerializer
#     parser_classes = [JSONParser, MultiPartParser, FormParser]


class CarBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBooking.objects.prefetch_related('people', 'car').all()
    serializer_class = CarBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
