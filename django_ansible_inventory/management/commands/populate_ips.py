import ipaddress
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate IP addresses for a given IP network"

    def add_arguments(self, parser):
        parser.add_argument(
            "network_name", type=str, help="The name of the IP network to populate"
        )

    def handle(self, *args, **kwargs):
        from django.apps import apps

        NetworkLabel = apps.get_model("django_ansible_inventory", "NetworkLabel")
        NetworkAddress = apps.get_model("django_ansible_inventory", "NetworkAddress")

        network_name = kwargs["network_name"]
        try:
            network_label = NetworkLabel.objects.get(name=network_name)
            network = ipaddress.ip_network(network_label.network)

            ip_addresses = []
            for ip in network.hosts():
                if not NetworkAddress.objects.filter(
                    ip_address=str(ip), network_label=network_label
                ).exists():
                    ip_addresses.append(
                        NetworkAddress(ip_address=str(ip), network_label=network_label)
                    )

            NetworkAddress.objects.bulk_create(ip_addresses)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully populated IP addresses for {network_name}"
                )
            )

        except NetworkLabel.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"NetworkLabel with name {network_name} does not exist"
                )
            )
