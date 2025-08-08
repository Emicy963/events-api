from django.urls import path
from . import views


urlpatterns = [
    path("", views.EventListCreateView.as_view(), name="event_list_create"),
    path("slug:slug/", views.EventDetailView.as_view(), name="event_detail"),
    path("location/search/", views.events_by_location, name="events_by_location"),
]
