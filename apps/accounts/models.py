from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.cores.models import TimestampedModel, StatusChoices

class UserTypeChoices(models.TextChoices):
    ORGANIZER = 'organizer', 'Organizador'
    BUYER = 'buyer', 'Comprador'
    BOTH = 'both', 'Ambos'

class User(AbstractUser, TimestampedModel):
    """Usuário customizado"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices)
    preferred_language = models.CharField(max_length=5, default='pt-ao')
    preferred_currency = models.CharField(max_length=3, default='AOA')
    is_verified = models.BooleanField(default=False)
    # Social Auth
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']
