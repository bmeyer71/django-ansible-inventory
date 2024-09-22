from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Host, NetworkLabel
from .management.commands.populate_ips import Command


@receiver(post_delete, sender=Host)
def mark_ip_available(sender, instance, **kwargs):
    # Mark the associated IP address as available after host deletion
    if instance.ip_address:
        instance.ip_address.is_assigned = False
        instance.ip_address.save()


@receiver(post_save, sender=NetworkLabel)
def auto_populate_ips(sender, instance, created, **kwargs):
    if created:
        # Automatically run the management command for the new IP Network
        command = Command()
        command.handle(network_name=instance.name)
