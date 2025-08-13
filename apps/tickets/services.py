from decimal import Decimal
from apps.tickets.models import TicketType


class TicketService:
    """Serviços relacionados a ingressos"""

    @staticmethod
    def creator_order(buyer, event_id, ticket_items, buyer_data):
        """Criar pedido de compra"""
        # Calcular totais
        subtotal = Decimal("0.00")
        items_to_create = []

        for item in ticket_items:
            ticket_type = TicketType.objects.get(id=item["ticket_type_id"])
            quantity = item["quantity"]

            # Verificar disponibilidade
            if ticket_type.quantity_available < quantity:
                raise ValueError(f"Not enough tickets available for {ticket_type.name}")
            
            # Verificar limites por pedido
            if quantity < ticket_type.min_quantity_per_order or quantity > ticket_type.max_quantity_per_order:
                raise ValueError(f"Invalid quantity for {ticket_type.name}")
            
            item_total = ticket_type.price_aoa * quantity
            subtotal += item_total

            items_to_create.append({
                "ticket_type": ticket_type,
                "quantity": quantity,
                "unit_price": ticket_type.price_aoa
            })
