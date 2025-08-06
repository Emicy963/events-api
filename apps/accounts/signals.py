from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, OrganizerProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria um UserProfile sempre que um User é criado."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o UserProfile quando o User é salvo."""
    if hasattr(instance, "profile"):
        instance.profile.save()


@receiver(post_save, sender=User)
def create_organizer_profile(sender, instance, created, **kwargs):
    """Cria um OrganizerProfile se o user_type for 'organizer' ou 'both'."""
    if created and instance.user_type in ["organizer", "both"]:
        OrganizerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_organizer_profile(sender, instance, **kwargs):
    """Salva o OrganizerProfile quando o User é salvo."""
    if instance.user_type in ["organizer", "both"] and hasattr(
        instance, "organizer_profile"
    ):
        instance.organizer_profile.save()
