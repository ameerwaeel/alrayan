from django.urls import path
from .views import *


urlpatterns = [
    path('ContactUs/', ContactUsAPIView.as_view(), name='ContactUs'),
    path('Newsletter/', NewsletterAPIView.as_view(), name='Newsletter'),
    path('find_us/', FindUsListCreateView.as_view(), name='find_us'),
    path('get_in_touch/', GetInTouchListCreateView.as_view(), name='get_in_touch'),
]



