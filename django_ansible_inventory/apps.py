from django.apps import AppConfig


class DjangoAnsibleInventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_ansible_inventory"
    verbose_name = "Ansible Inventory"

    def ready(self):
        # Import signals here
        from . import signals
