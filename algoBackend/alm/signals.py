from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BondPortofolio

@receiver(pre_save, sender=BondPortofolio)
def ensure_single_active_portofolio(sender, instance, **kwargs):
    if instance.is_active:
        BondPortofolio.objects.filter(user=instance.user, is_active=True).update(is_active=False)
