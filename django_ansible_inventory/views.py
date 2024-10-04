from rest_framework import generics
from .serializers import HostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Dict, Any
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import NetworkAddress, Host


def get_available_ips(request):
    vlan_id = request.GET.get("vlan", None)
    selected_ip = request.GET.get(
        "selected_ip", None
    )  # Pass the selected IP when editing

    if vlan_id:
        # Clean up expired reservations
        NetworkAddress.objects.filter(
            is_reserved=True,
            reservation_timestamp__lt=timezone.now() - timedelta(minutes=10),
        ).update(
            is_reserved=False,
            reserved_by=None,
            reservation_timestamp=None,
        )

        available_ips = NetworkAddress.objects.filter(
            network_label_id=vlan_id,
            is_assigned=False,
            is_reserved=False,
        ).order_by("pk")[:5]
        ip_data = [{"id": ip.id, "ip_address": ip.ip_address} for ip in available_ips]

        # If the selected IP is assigned, add it manually
        if selected_ip:
            try:
                selected_ip_obj = NetworkAddress.objects.get(id=selected_ip)
                ip_data.append(
                    {"id": selected_ip_obj.id, "ip_address": selected_ip_obj.ip_address}
                )
            except NetworkAddress.DoesNotExist:
                pass

        return JsonResponse({"available_ips": ip_data})

    return JsonResponse({"available_ips": []})


class HostListView(generics.ListAPIView):
    queryset = Host.objects.filter(enabled=True)
    serializer_class = HostSerializer


class AnsibleInventoryView(APIView):
    def get(self, request, format=None):
        tag = request.query_params.get("tag", None)
        if tag:
            hosts = Host.objects.filter(enabled=True, groups__tags__name=tag).distinct()
        else:
            hosts = Host.objects.filter(enabled=True)

        # Define the type of inventory to guide the linter
        inventory: Dict[str, Dict[str, Any]] = {"_meta": {"hostvars": {}}}

        for host in hosts:
            for group in host.groups.all():
                group_name = group.name
                group_vars = group.group_vars

                if group_name not in inventory:
                    inventory[group_name] = {
                        "hosts": [],
                        "vars": group_vars,
                    }

                # Ensure Pylance knows this is a list
                inventory[group_name]["hosts"].append(
                    {
                        "name": host.name,
                        "vars": host.host_vars,
                    }
                )

                # Add host variables to _meta
                inventory["_meta"]["hostvars"][host.name] = host.host_vars

        return Response(inventory)
