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
from django.core.mail import EmailMessage
import threading
import logging

from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
# from .utils import send_booking_email

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

# class BookingListCreateView(generics.ListCreateAPIView):
#     # queryset = Booking.objects.prefetch_related('people').select_related('country').all()
#     queryset = Booking.objects.prefetch_related('people').all()
#     serializer_class = BookingSerializer
#     parser_classes = [JSONParser, MultiPartParser, FormParser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         booking = serializer.save()

#         # booking = Booking.objects.prefetch_related('people', 'country').get(pk=booking.pk)
#         booking = Booking.objects.prefetch_related('people').get(pk=booking.pk)

#         return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)

# class BookingListCreateView(generics.ListCreateAPIView):
#     queryset = Booking.objects.prefetch_related('people').all()
#     serializer_class = BookingSerializer
#     parser_classes = [JSONParser, MultiPartParser, FormParser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         booking = serializer.save()

#         # جلب الأشخاص المرتبطين بالحجز
#         booking = Booking.objects.prefetch_related('people__nationality').get(pk=booking.pk)

#         # إعداد محتوى الإيميل
#         subject = f"New Booking - Travel on {booking.travel_date}"
#         body = f"""
# تم إنشاء حجز جديد:

# • تاريخ السفر: {booking.travel_date}
# • تاريخ العودة: {booking.return_date}
# • عدد البالغين: {booking.adults}
# • عدد الأطفال: {booking.children}
# • السعر الإجمالي: {booking.total_price} USD

# المسافرون:
# """
#         for person in booking.people.all():
#             body += f"""
#     - الاسم: {person.full_name}
#       البريد: {person.email}
#       الجنسية: {person.nationality.country}
#       العمر: {person.age}
#       الهاتف: {person.phone}
# """

#         # الإيميل المرسل سيكون من أول شخص فقط (لو موجود)
#         from_email = booking.people.first().email if booking.people.exists() else "noreply@example.com"

#         send_booking_email(subject, body, from_email)

#         return Response(self.get_serializer(booking).data, status=status.HTTP_201_CREATED)
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.prefetch_related('people__nationality').all()
    serializer_class = BookingSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # إعادة جلب الحجز مع التفاصيل المطلوبة
        booking = Booking.objects.prefetch_related('people__nationality').get(pk=booking.pk)

        # إعداد محتوى الإيميل
        subject = f"New Visa Booking - Travel on {booking.travel_date}"
        body = f"""
تم إنشاء حجز جديد:

• تاريخ الإنشاء: {booking.created_at}
• آخر تعديل: {booking.updated_at}
• تاريخ السفر: {booking.travel_date}
• تاريخ العودة: {booking.return_date}
• عدد البالغين: {booking.adults}
• عدد الأطفال: {booking.children}
• إجمالي الأشخاص: {booking.total_people}
• السعر الإجمالي: {booking.total_price} 

• تفاصيل الرحلة: {booking.flight_info}
• تفاصيل الفندق: {booking.hotel_info}

المسافرون:
"""

        for person in booking.people.all():
            nationality = person.nationality
            flag_url = request.build_absolute_uri(nationality.flag_image.url) if nationality.flag_image else "N/A"
            visa_img = request.build_absolute_uri(person.visa_image.url) if person.visa_image else "N/A"
            image_url = request.build_absolute_uri(person.image.url) if person.image else "N/A"

            body += f"""
    - الاسم: {person.full_name}
      البريد: {person.email}
      العنوان: {person.address}
      الجنسية: {nationality.country}
      نوع الفيزا: {nationality.visa_type}
      سعر الفيزا: {nationality.price} 
      صورة العلم: {flag_url}
      العمر: {person.age}
      الهاتف: {person.phone}
      صورة شخصية: {image_url}
      صورة الفيزا: {visa_img}
      تاريخ الإضافة: {person.created_at}
      آخر تحديث: {person.updated_at}
"""

        # الإيميل المرسل سيكون من أول شخص فقط (لو موجود)
        from_email = booking.people.first().email if booking.people.exists() else "noreply@example.com"

        send_booking_email(subject, body, from_email)

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

