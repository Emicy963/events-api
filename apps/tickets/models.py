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
