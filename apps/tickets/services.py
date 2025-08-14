from decimal import Decimal
import uuid
from django.utils import timezone
from apps.tickets.models import Order, Ticket, TicketType


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

            # Calcular taxas (5% da plataforma)
            fees = subtotal * Decimal("0.05")
            total = subtotal + fees

            # Criar pedido
            order = Order.objects.create(
                buyer=buyer,
                event_id=event_id,
                order_number=TicketService.generate_order_number(),
                subtotal_aoa=subtotal,
                fees_aoa=fees,
                total_aoa=total,
                buyer_name=buyer_data["name"]
                buyer_email=buyer_data["email"]
                buyer_phone=buyer_data["phone"]
            )

            # Criar tickets
            for item in items_to_create:
                ticket_type = item["ticket_type"]
                quantity = item["quantity"]

                for _ in range(quantity):
                    ticket = Ticket.objects.create(
                        order=order,
                        ticket_type=ticket_type,
                        ticket_number=TicketService.generate_ticket_number(),
                        qr_data=QRCodeService.generate_qr_data(order, ticket_type)
                    )
                    # Gerar QR Code
                    ticket.generate_qr_code()
                    ticket.save()
                
                # Atualizar quantidade vendida
                ticket_type.quantity_sold += quantity
                ticket_type.save()
        return order

    @staticmethod
    def generate_order_number():
        """Gerar número único do pedido"""
        return f"EAO{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:10].upper}"
