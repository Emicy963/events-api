from django.db import models
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
