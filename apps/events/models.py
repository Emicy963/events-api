from django.db import models
from apps.cores.models import TimestampedModel, StatusChoices

class EventCategory(TimestampedModel):
    """Categorias de eventos populares em Angola"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True) # Font Awesome class

    class Meta:
        verbose_name_plural = "Event Categories"
