from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import render, get_object_or_404 
from .models import *
from .serializers import *
from django.core.mail import EmailMessage
from rest_framework import generics, status 
from rest_framework import generics
from .models import Find_Us, Get_In_Touch
from .serializers import FindUsSerializer, GetInTouchSerializer
import threading
from django.core.mail import EmailMessage
import logging
from rest_framework.parsers import MultiPartParser, FormParser

logger = logging.getLogger(__name__)  

def send_form_email(subject, body, from_email, file_path=None):
    def send_email():
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=["mrseller.prof@gmail.com"],
            )
            if file_path:
                email.attach_file(file_path)
            email.send()
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    threading.Thread(target=send_email).start()

# Create your views here.

class ContactUsAPIView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    def perform_create(self, serializer):
        instance = serializer.save()
        subject = "New Contact Us Form Submission"
        body = f"""
        full name: {instance.full_name}
        phone: {instance.phone}
        email: {instance.email}
        country : {instance.country}
        message: {instance.message}
        """
        success = send_form_email(subject, body, instance.email)

        if success:
            return Response({"message": "The active email has been sent!"}, status=status.HTTP_200_OK) 
        return Response({"error": "An error occurred while sending the email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsletterAPIView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = "New Newsletter Subscription"
        body = f"New subscription from: {instance.email}"
        success = send_form_email(subject, body, instance.email)

        if success:
            return Response({"message": "The active email has been sent!"}, status=status.HTTP_200_OK)
        return Response({"error": "An error occurred while sending the email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class FindUsListCreateView(generics.ListCreateAPIView):
    queryset = Find_Us.objects.prefetch_related('description').all()
    serializer_class = FindUsSerializer


class GetInTouchListCreateView(generics.ListCreateAPIView):
    queryset = Get_In_Touch.objects.prefetch_related("description")
    serializer_class = GetInTouchSerializer