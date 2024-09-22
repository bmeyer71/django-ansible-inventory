from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin

from .management.commands.populate_ips import Command


@admin.action(description="Populate IP addresses")
def populate_ips(modeladmin, request, queryset):
    command = Command()
    for network_label in queryset:
        command.handle(network_name=network_label.name)
    modeladmin.message_user(request, "IP addresses populated successfully.")


@admin.action(description="Mark selected as DEFAULT")
def mark_default(modeladmin, request, queryset):
    ct = ContentType.objects.get_for_model(queryset.model)
    obj_model = ct.model_class()
    model_default = obj_model.objects.get(item_default=True)
    if queryset.count() == 1:
        for obj in queryset:
            if obj.admin_only is True:
                obj.item_default = False
                messages.error(
                    request, "Item can not be set as default if 'Admin only' is set."
                )
            else:
                obj.item_default = True
                obj.save()
                model_default.item_default = False
                model_default.save()
                messages.success(request, "Successfully marked as Default.")
    else:
        messages.error(request, "Only one item can be set as Default.")


@admin.action(description="Mark selected ENABLED")
def mark_enabled(modeladmin, request, queryset):
    queryset.update(
        deprecated=False,
        enabled=True,
    )
    messages.success(request, "Successfully ENABLED selected.")


@admin.action(description="Mark selected as DISABLED")
def mark_disabled(modeladmin, request, queryset):
    queryset.update(enabled=False)
    messages.success(request, "Successfully DISABLED selected.")


@admin.action(description="Mark selected DEPRECATED")
def mark_deprecated(modeladmin, request, queryset):
    queryset.update(deprecated=True)
    messages.success(request, "Successfully marked selected as DEPRECATED.")
