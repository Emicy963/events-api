from django.contrib.auth.models import AbstractUser

# from django.contrib.gis.db import models as gis_models
from django.db import models
from apps.cores.models import TimestampedModel, StatusChoices


class UserTypeChoices(models.TextChoices):
    ORGANIZER = "organizer", "Organizador"
    BUYER = "buyer", "Comprador"
    BOTH = "both", "Ambos"


class User(AbstractUser, TimestampedModel):
    """Usuário customizado"""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices)
    preferred_language = models.CharField(max_length=5, default="pt-ao")
    preferred_currency = models.CharField(max_length=3, default="AOA")
    is_verified = models.BooleanField(default=False)
    # Social Auth
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]


class UserProfile(TimestampedModel):
    """Perfil estendido do usuário"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    # Localização (Angola)
    province = models.CharField(max_length=50, blank=True)
    municipality = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    # location = gis_models.PointField(blank=True, null=True) # Coordenadas GPS
    location = models.CharField(max_length=255, blank=True, null=True)
    # Configurações
    sms_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)


class OrganizerProfile(TimestampedModel):
    """Perfil específico para organizadores"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="organizer_profile"
    )
    company_name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, unique=True)  # NIF em Angola
    company_logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    # Verificação
    is_verified = models.BooleanField(default=False)
    verification_documents = models.JSONField(default=dict)
    # Comissões
    comission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    total_events = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
