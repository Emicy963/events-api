from django.utils import timezone
from rest_framework import generics
from .models import TicketType
from .serializers import TicketTypeSerializer

class TicketTypeListView(generics.ListAPIView):
    """Lista tipos de ingresso de um evento"""
    serializer_class = TicketTypeSerializer

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return TicketType.objects.filter(
            event_id=event_id,
            is_active=True,
            sale_start__lte=timezone.now(),
            sale_end_gte=timezone.now()
        )
