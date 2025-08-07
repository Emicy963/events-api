from django.db import models
from apps.cores.models import TimestampedModel, StatusChoices
from django.conf import settings


class EventCategory(TimestampedModel):
    """Categorias de eventos populares em Angola"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome class

    class Meta:
        verbose_name_plural = "Event Categories"


class Event(TimestampedModel):
    """Evento principal"""

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)

    # Information about the event
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)

    # Visual
    cover_image = models.ImageField(upload_to="events/covers/")
    gallery = models.JSONField(default=list)  # Lista de URLS de imagens

    # Data e local
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50, default="Africa/Luanda")

    # Localização
    venue_name = models.CharField(max_length=255)
    venue_address = models.TextField()
    province = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    # Configurações
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    is_featured = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)  # Evento privado
    requires_approval = models.BooleanField(default=False)  # Aprovação manual

    # Limites
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    min_age = models.PositiveIntegerField(blank=True, null=True)

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    tickets_sold = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class EventTeamMember(TimestampedModel):
    """Equipe do evento"""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="team",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=50)  # Admin, Moderator, Validator
    permissions = models.JSONField(default=dict)
