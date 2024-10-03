from django import forms
from netaddr import IPAddress as NetIPAddress, IPNetwork
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from .models import Host, NetworkAddress


class HostAdminForm(forms.ModelForm):
    use_manual_ip = forms.BooleanField(
        required=False,
        label="Manually enter IP",
    )
    manual_ip = forms.GenericIPAddressField(
        required=False,
        label="Manual IP Address",
    )

    class Meta:
        model = Host
        fields = "__all__"
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

        user = self.current_user

        # Clean up expired reservations
        NetworkAddress.objects.filter(
            is_reserved=True,
            reservation_timestamp__lt=timezone.now() - timedelta(minutes=10),
        ).update(is_reserved=False, reserved_by=None, reservation_timestamp=None)

        # Get VLAN ID from form data or instance
        if "vlan" in self.data and self.data.get("vlan"):
            vlan_id = self.data.get("vlan")
        elif self.instance.pk and self.instance.vlan:
            vlan_id = self.instance.vlan.id
        else:
            vlan_id = None

        # Set up the queryset for ip_address field
        if vlan_id:
            # Build the base queryset
            queryset = NetworkAddress.objects.filter(
                network_label_id=vlan_id, is_assigned=False
            ).filter(Q(is_reserved=False) | Q(reserved_by=user))

            # Include the selected IP in the queryset
            selected_ip_id = self.data.get("ip_address") or self.initial.get(
                "ip_address"
            )
            if selected_ip_id:
                queryset = queryset | NetworkAddress.objects.filter(pk=selected_ip_id)

            self.fields["ip_address"].queryset = queryset.distinct()
        else:
            self.fields["ip_address"].queryset = NetworkAddress.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        use_manual_ip = cleaned_data.get("use_manual_ip")
        manual_ip = cleaned_data.get("manual_ip")
        ip_address = cleaned_data.get("ip_address")
        vlan = cleaned_data.get("vlan")

        # Handle manual IP entry
        if use_manual_ip:
            if manual_ip:
                # Ensure the manual IP is valid within the selected VLAN's network
                if vlan:
                    network = IPNetwork(vlan.network)
                    if NetIPAddress(manual_ip) not in network:
                        raise forms.ValidationError(
                            f"The IP {manual_ip} is not valid for the selected network {vlan.network}."
                        )

                    # Check if the IP address is already assigned
                    if NetworkAddress.objects.filter(
                        ip_address=manual_ip, is_assigned=True
                    ).exists():
                        raise forms.ValidationError(
                            f"The IP address {manual_ip} is already assigned to another host."
                        )

                    # If the IP is valid and not assigned, create or retrieve it
                    ip, created = NetworkAddress.objects.get_or_create(
                        ip_address=manual_ip,
                        defaults={"is_assigned": True, "network_label": vlan},
                    )
                    cleaned_data["ip_address"] = (
                        ip  # Assign the manually entered IP to the form
                    )
                else:
                    raise forms.ValidationError(
                        "Please select a VLAN before entering an IP address."
                    )
            else:
                raise forms.ValidationError("Please enter a valid IP address manually.")
        else:
            if not ip_address:
                raise forms.ValidationError(
                    "Please select an IP address from the list."
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        ip_address = self.cleaned_data.get("ip_address")

        # If editing an existing instance, unassign the old IP
        if instance.pk:
            old_instance = Host.objects.get(pk=instance.pk)
            old_ip = old_instance.ip_address
            if old_ip and old_ip != ip_address:
                # Unassign the old IP
                old_ip.is_assigned = False
                old_ip.save()

        if ip_address:
            # Assign the new IP
            ip_address.is_assigned = True
            ip_address.is_reserved = False
            ip_address.reserved_by = None
            ip_address.reservation_timestamp = None
            ip_address.save()

        if commit:
            instance.save()
            self.save_m2m()

        return instance
