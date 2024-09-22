from rest_framework import serializers
from django_ansible_inventory.models import AnsibleGroup, Host


class AnsibleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsibleGroup
        fields = ["name", "tags", "group_vars"]


class HostSerializer(serializers.ModelSerializer):
    groups = AnsibleGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Host
        fields = ["name", "ip_address", "enabled", "groups", "host_vars"]
