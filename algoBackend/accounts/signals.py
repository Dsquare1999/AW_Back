import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from bilan.models import Bilan
from alm.models import BondPortofolio
from accounts.models import Profile
from room.models import Room
from accounts.models import User

# Configurer le logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_bilan_for_new_user(sender, instance, created, **kwargs):
    logger.info("Signal launched")  # Logging pour vérifier le lancement du signal
    if created:
        logger.info("Signal triggered for: %s", instance.email)  # Logging pour vérifier le déclenchement du signal
        Profile.objects.create(user=instance)
        bilan = Bilan.objects.create(user=instance, is_active=True, is_simulated=False)
        BondPortofolio.objects.create(user=instance, bilan=bilan, is_active=True, name="Bonds Portofolio "+instance.email)
        algo_friend = User.objects.filter(email='algofriend@algoway.com').first()
        if algo_friend:
            room = Room.objects.create(name="Algo Friend Room")
            room.participants.set([instance, algo_friend])
            room.save()

        else:
            logger.info("Algo friend user not found.")  # Logging pour vérifier la présence de l'utilisateur "algofriend"
