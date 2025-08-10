import qrcode
from django.db import models
from django.conf import settings
from django.core.files import File
from io import BytesIO
from apps.cores.models import TimestampedModel

class TicketTypeChoices(models.TextChoices):
    FREE = "free", "Gratuito"
    PAID = "paid", "Pago"
    DONATAION = "donation", "Doação"

class TickeType(TimestampedModel):
    """Tipos de ingresso"""
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="ticket_types"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Preço
    type = models.CharField(
        max_length=20, choices=TicketTypeChoices.choices
    )
    price_aoa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Disponibilidade
    quantity_total = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    sale_start = models.DateTimeField()
    sale_end = models.DateTimeField()

    # Configurações
    min_quantity_per_order = models.PositiveBigIntegerField(default=1)
    max_quantity_per_order = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    @property
    def quantity_available(self):
        return self.quantity_total - self.quantity_sold
    
    @property
    def is_sold_out(self):
        return self.quantity_available <= 0

class Order(TimestampedModel):
    """Pedido de compra"""
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    # Identificação
    order_number = models.CharField(
        max_length=2, unique=True
    )

    # Valores
    subtotal_aoa = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    fees_aoa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_aoa = models.DecimalField(
        max_digits=20, decimal_places=2
    )
    currency = models.CharField(max_length=3, default="AOA")

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pendente"),
            ("paid", "Pago"),
            ("failed", "Falhou"),
            ("cancelled", "Cancelado"),
            ("refunded", "Reembolso"),
        ], default="pending"
    )

    # Dados do comprador
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=20)

    # Payment
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)

class Ticket(TimestampedModel):
    """Ingresso individual"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    ticket_type = models.ForeignKey(
        TickeType, on_delete=models.CASCADE
    )
    
    # Identificação única
    ticket_number = models.CharField(max_length=20, unique=True)
    qr_code = models.ImageField(upload_to="qr_code/", blank=True, null=True)
    qr_data = models.TextField() # Dados criptogrfados

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("valid", "Válido"),
            ("used", "Usado"),
            ("expired", "Expirado"),
            ("cancelled", "Cancelado"),
        ], default="valid"
    )

    # Validação
    used_at = models.DateTimeField(blank=True, null=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="validated_tickets"
    )

    def generate_qr_code(self):
        """Gera QR code para o ingresso"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        filename = f"qr_{self.ticket_number}.png"
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()
