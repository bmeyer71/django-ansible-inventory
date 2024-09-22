from django.urls import path
from .views import get_available_ips

urlpatterns = [
    path(
        "get-available-ips/",
        get_available_ips,
        name="get_available_ips",
    ),
]
