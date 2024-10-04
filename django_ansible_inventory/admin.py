from django.contrib import admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

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
        "host_type",
    )
    filter_horizontal = ("groups",)
    list_filter = [
        "enabled",
        "host_type",
        "environment",
        "host_class",
        "purpose",
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
            "admin/js/ip_reserve.js",
        )
        css = {"all": ("admin/css/custom_select2.css",)}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            kwargs["help_text"] = "Use Ctrl + Click to select multiple groups"
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "reserve-ip/",
                self.admin_site.admin_view(self.reserve_ip),
                name="reserve_ip",
            ),
            path(
                "release-ip/",
                self.admin_site.admin_view(self.release_ip),
                name="release_ip",
            ),
        ]
        return custom_urls + urls

    # Remove @csrf_exempt to enable CSRF protection
    def reserve_ip(self, request):
        if request.method == "POST":
            ip_id = request.POST.get("ip_id")
            user = request.user

            try:
                ip = NetworkAddress.objects.get(pk=ip_id)

                # Check if the IP is already assigned or reserved by someone else
                if ip.is_assigned:
                    return JsonResponse(
                        {"success": False, "message": "IP is already assigned."}
                    )
                if (
                    ip.is_reserved
                    and ip.reserved_by != user
                    and not ip.is_reservation_expired()
                ):
                    return JsonResponse(
                        {"success": False, "message": "IP is reserved by another user."}
                    )

                # Reserve the IP
                ip.is_reserved = True
                ip.reserved_by = user
                ip.reservation_timestamp = timezone.now()
                ip.save()

                return JsonResponse({"success": True})

            except NetworkAddress.DoesNotExist:
                return JsonResponse({"success": False, "message": "IP does not exist."})
        else:
            return JsonResponse(
                {"success": False, "message": "Invalid request method."}
            )

    @csrf_exempt  # Exempt from CSRF checks for release_ip
    def release_ip(self, request):
        if request.method == "POST":
            ip_id = request.POST.get("ip_id")
            user = request.user if request.user.is_authenticated else None

            try:
                ip = NetworkAddress.objects.get(pk=ip_id)

                # Check if the IP is reserved by the current user or if the reservation has expired
                if ip.reserved_by == user or ip.is_reservation_expired():
                    ip.is_reserved = False
                    ip.reserved_by = None
                    ip.reservation_timestamp = None
                    ip.save()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "You do not have permission to release this IP.",
                        }
                    )
            except NetworkAddress.DoesNotExist:
                return JsonResponse({"success": False, "message": "IP does not exist."})
        else:
            return JsonResponse(
                {"success": False, "message": "Invalid request method."}
            )


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
        "network_label",
        "is_assigned",
        "is_reserved",
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
