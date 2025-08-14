from django.utils import timezone
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ticket, TicketType
from .services import TicketService
from .serializers import TicketSerializer, TicketTypeSerializer, OrderCreateSerializer

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
                order = TicketService.creator_order(buyer=request.user)
                event_id = request.data.get("event_id")
                ticket_items = serializer.validated_data["ticket_items"],
                buyer_data = {
                    "name": serializer.validated_data["buyer_name"],
                    "email": serializer.validated_data["buyer_email"],
                    "phone": serializer.validated_data["buyer_phone"]
                }
                return Response({
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "total": order.total_aoa,
                    "payment_url": f"/api/payments/{order.id}/process/"
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def my_tickets(request):
    """Meus ingressos"""
    tickets = Ticket.objects.filter(
        order__buyer=request.user,
        order__status="paid"
    ).select_related("ticket_type", "ticket_type__event", "order")
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)
