from django.db.models.signals import post_save
from django.dispatch import receiver

from zedasignal_backend.apps.trading.models import Signal
from zedasignal_backend.apps.trading.services import SignalService


@receiver(post_save, sender=Signal)
def publish_signals_to_active_users_by_email(sender, instance: Signal, created, **kwargs):
    """
    This method sends signals to active users by email.
    """
    if created:
        SignalService.publish_signal_to_active_subscribers_by_email(instance)
