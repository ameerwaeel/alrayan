
from django.urls import path
from .views import *

urlpatterns = [
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),

    path('car-images/', CarImageListCreateView.as_view(), name='car-image-list'),

    path('categories/', CarCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CarCategoryDetailView.as_view(), name='category-detail'),

    path('car-bookings/', CarBookingListCreateView.as_view(), name='car-booking-list'),
    path('car-bookings/<int:pk>/', CarBookingDetailView.as_view(), name='car-booking-detail'),
]
