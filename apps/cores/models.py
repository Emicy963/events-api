from django.db import models
import uuid


class TimestampedModel(models.Model):
    """Modelo base com timestamps"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusChoices(models.TextChoices):
    ACTIVE = "active", "Ativo"
    INACTIVE = "inactive", "Inativo"
    PENDING = "pending", "Pendente"
    CANCELLED = "cancelled", "Cancelado"
