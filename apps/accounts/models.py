from django.db import models

class UserTypeChoices(models.TextChoices):
    ORGANIZER = 'organizer', 'Organizador'
    BUYER = 'buyer', 'Comprador'
    BOTH = 'both', 'Ambos'
