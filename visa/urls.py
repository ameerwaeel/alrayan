from django.urls import path
from .views import *

urlpatterns = [
    path('create-booking/', BookingListCreateView.as_view(), name='create-booking'),
    path('create-booking/<int:pk>/', BookingDetailView.as_view()),
    path('visa-sections/', VisaSectionListCreateView.as_view(), name='visa-sections'),
    path('visa-sections/<int:pk>/', VisaSectionDetailView.as_view()),
    path('countries/', CountryListCreateView.as_view(), name='countries'),
    path('countries/<int:pk>/', CountryDetailView.as_view()),
    path('country-list/', CountryListView.as_view(), name='country-list'),
    path('visa-cards/', VisaCardListCreateView.as_view(), name='visa-cards'),
    path('visa-cards/<int:pk>/', VisaCardDetailView.as_view(), name='visa-card-detail'),




]


