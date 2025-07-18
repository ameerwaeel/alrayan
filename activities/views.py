from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
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

# class ActivityBookingListCreateView(generics.ListCreateAPIView):
#     queryset = ActivityBooking.objects.prefetch_related('people')
#     serializer_class = ActivityBookingSerializer
#     parser_classes = [JSONParser, MultiPartParser, FormParser]
class ActivityBookingListCreateView(generics.ListCreateAPIView):
    queryset = ActivityBooking.objects.prefetch_related('people')
    serializer_class = ActivityBookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # جلب الحجز مع الأشخاص
        booking = ActivityBooking.objects.prefetch_related('people').get(pk=booking.pk)

        subject = f"Activity Booking - {booking.activity} on {booking.datebooking}"
        body = f"""
تم إنشاء حجز نشاط جديد:

• النشاط: {booking.activity}
• تاريخ الحجز: {booking.datebooking}
• عدد البالغين: {booking.adults}
• عدد الأطفال: {booking.children}
• عدد الأشخاص: {booking.total_people}
• السعر الإجمالي: {booking.total_price} 

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
