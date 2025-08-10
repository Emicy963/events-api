from rest_framework import serializers
from .models import TicketType, Order


class TicketTypeSerializer(serializers.ModelSerializer):
    quantity_available = serializers.IntegerField(read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TicketType
        fields = "__all__"

class OrderCreateSerializer(serializers.ModelSerializer):
    ticket_items = serializers.JSONField(write_only=True) # [{"ticket_type_id": 1, "quantity": 2}]
    class Meta:
        model = Order
        fields = ["ticket_items", "buyer_name", "buyer_email", "buyer_phone"]
