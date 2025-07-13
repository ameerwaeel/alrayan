from django.urls import path
from .views import ScrapeLegendOfMoscowView
from .views import ScrapeRoomsView,ScrapeRoomView,SubmitRoomSearchView

urlpatterns = [
    path('scrape/', ScrapeLegendOfMoscowView.as_view(), name='scrape-legend'),
    path("scrape-rooms/", ScrapeRoomView.as_view()),
    path("scrape-rooms1/", ScrapeRoomsView.as_view()),
    path("search/", SubmitRoomSearchView.as_view()),

]