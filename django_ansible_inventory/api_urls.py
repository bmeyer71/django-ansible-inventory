from django.urls import path
from .views import HostListView, AnsibleInventoryView

urlpatterns = [
    path(
        "hosts/",
        HostListView.as_view(),
        name="host-list",
    ),
    path(
        "inventory/",
        AnsibleInventoryView.as_view(),
        name="host-management",
    ),
]
