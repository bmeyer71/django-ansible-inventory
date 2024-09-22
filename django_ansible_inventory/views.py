from django.http import JsonResponse
from .models import NetworkAddress


def get_available_ips(request):
    vlan_id = request.GET.get("vlan", None)
    selected_ip = request.GET.get(
        "selected_ip", None
    )  # Pass the selected IP when editing

    if vlan_id:
        available_ips = NetworkAddress.objects.filter(
            network_label_id=vlan_id, is_assigned=False
        )[:5]
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
