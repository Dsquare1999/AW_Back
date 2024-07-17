from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Bilan

@receiver(pre_save, sender=Bilan)
def ensure_single_active_bilan(sender, instance, **kwargs):
    if instance.is_active:
        Bilan.objects.filter(user=instance.user, is_active=True).update(is_active=False)
