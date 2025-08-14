from django.utils import timezone
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import TicketType
from .serializers import TicketTypeSerializer, OrderCreateSerializer

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

@api_view(["POST"])
def create_order(request):
    """Criar pedidos"""
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                order = Ticke
