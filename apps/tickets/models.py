from django.db import models

class TicketTypeChoices(models.TextChoices):
    FREE = "free", "Gratuito"
    PAID = "paid", "Pago"
    DONATAION = "donation", "Doação"
