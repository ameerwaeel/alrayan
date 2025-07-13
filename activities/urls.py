from django.urls import path
from .views import *

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view()),
    path('categories/', ActivityCategoryListCreateView.as_view()),
    path('images/', ActivityImageListCreateView.as_view()),
    path('bookings/', ActivityBookingListCreateView.as_view()),
]
