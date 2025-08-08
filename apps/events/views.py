from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from .models import Event
from .serializers import EventCreateSerializer, EventSerializer

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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        return EventSerializer
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro por proximidade (GPS)
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 50)  # km
        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = queryset.filter(
	            location__distance_lte=(point, Distance(km=radius))
	        ).distance(point).order_by('distance')
        
        # Filtro por data
        date_from = self.reques.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from:
            queryset = queryset.filter(start_datetime__gte=date_from)
        if date_to:
            queryset = queryset.filter(start_datetime__lte=date_to)
        
        return queryset
