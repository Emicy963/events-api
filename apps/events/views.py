from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from .models import Event
from .serializers import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    """Lista e criação de eventos"""
    queryset = Event.objects.filter(status="active").select_related("organizer", "category")
    serializer_class = EventSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "category",
        "province",
        "municipality",
        "organizer",
    ]
    search_fields = ["title", "description", "venue_name"]
    ordering_fields = ["start_datetime", "created_at", "views_count"]

