from django import forms
from .models import Host, NetworkAddress
from netaddr import IPAddress as NetIPAddress, IPNetwork


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
            "short_description": forms.Textarea(
                attrs={"rows": 4, "cols": 40}
            ),  # Adjust rows/cols as needed
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the IP address dropdown based on VLAN selection
        if "vlan" in self.data:
            vlan_id = self.data.get("vlan")
            self.fields["ip_address"].queryset = NetworkAddress.objects.filter(
                network_label_id=vlan_id, is_assigned=False
            )

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
