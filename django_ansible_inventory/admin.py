from django.contrib import admin
from .models import (
    Host,
    AnsibleGroup,
    AnsibleGroupTag,
    NetworkAddress,
    NetworkLabel,
    HostType,
    Environment,
    Purpose,
    HostClass,
    HostStatus,
    BusinessUnit,
    SupportLevel,
    SupportGroup,
)
from .forms import HostAdminForm
from .actions import (
    populate_ips,
    mark_enabled,
    mark_disabled,
    mark_default,
    mark_deprecated,
)


@admin.register(AnsibleGroup)
class AnsibleGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("tags",)
    list_filter = ["tags"]
    ordering = ["name"]
    search_fields = ["name", "tags__name"]


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    form = HostAdminForm
    list_display = (
        "name",
        "ip_address",
        "enabled",
    )
    filter_horizontal = ("groups",)
    list_filter = [
        "enabled",
        "groups",
        "host_type",
    ]
    ordering = ["name"]
    fields = [
        "name",
        "enabled",
        "groups",
        "host_vars",
        "short_description",
        "host_type",
        "environment",
        "purpose",
        "host_status",
        "host_class",
        "business_unit",
        ("support_group", "support_level"),
        "vlan",
        "use_manual_ip",
        "manual_ip",
        "ip_address",
    ]
    autocomplete_fields = ["groups"]
    search_fields = [
        "name",
        "groups__name",
        "vlan__name",
        "ip_address__ip_address",
    ]

    class Media:
        js = (
            "admin/js/ip_filter.js",
            "admin/js/toggle_ip.js",
        )
        css = {"all": ("admin/css/custom_select2.css",)}

    def save_model(self, request, obj, form, change):
        if change:
            old_ip = Host.objects.get(pk=obj.pk).ip_address
            if old_ip and old_ip != obj.ip_address:
                old_ip.is_assigned = False
                old_ip.save()
        if obj.ip_address:
            obj.ip_address.is_assigned = True
            obj.ip_address.save()
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            kwargs["help_text"] = "Use Ctrl + Click to select multiple groups"
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(AnsibleGroupTag)
class AnsibleGroupTagAdmin(admin.ModelAdmin):
    ordering = ["name"]


@admin.register(NetworkLabel)
class NetworkLabelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "network",
        "enabled",
        "item_default",
        "deprecated",
    )
    list_filter = [
        "enabled",
        "deprecated",
    ]
    actions = [
        populate_ips,
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(NetworkAddress)
class NetworkAddressAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "network_label",
        "is_assigned",
    )
    list_filter = [
        "is_assigned",
        "network_label",
    ]
    search_fields = ["ip_address"]


@admin.register(HostType)
class HostTypeAdmin(admin.ModelAdmin):
    list_display = [
        "host_type",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "host_type",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["host_type"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = [
        "environment",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "environment",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["environment"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = [
        "purpose",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "purpose",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["purpose"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(HostClass)
class HostClassAdmin(admin.ModelAdmin):
    list_display = [
        "host_class",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "host_class",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["host_class"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(HostStatus)
class HostStatusAdmin(admin.ModelAdmin):
    list_display = [
        "host_status",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "host_status",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["host_status"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(BusinessUnit)
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = [
        "business_unit",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "business_unit",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["business_unit"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(SupportGroup)
class SupportGroupAdmin(admin.ModelAdmin):
    list_display = [
        "group",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "group",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["group"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]


@admin.register(SupportLevel)
class SupportLevelAdmin(admin.ModelAdmin):
    list_display = [
        "level",
        "enabled",
        "item_default",
        "deprecated",
    ]
    fields = [
        "level",
        "item_default",
        "enabled",
        "deprecated",
    ]
    ordering = ["level"]
    actions = [
        mark_enabled,
        mark_disabled,
        mark_default,
        mark_deprecated,
    ]
