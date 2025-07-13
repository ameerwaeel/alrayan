from django.urls import path
from .views import *
from django.urls import path
from .views import HeroSectionListCreateView, HeroSectionDetailView


urlpatterns = [
    path('hero-section/', HeroSectionListCreateView.as_view(), name='hero-section-list-create'),
    path('hero-section/<int:pk>/', HeroSectionDetailView.as_view(), name='hero-section-detail'),
    path('translated-texts/', TranslatedTextListCreateView.as_view(), name='translated-texts'),
    path('translated-texts/<int:pk>/', TranslatedTextDetailView.as_view(), name='translated-text-detail'),    
]