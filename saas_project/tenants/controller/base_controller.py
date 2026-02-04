from django.urls import path
from .tenant_controller import onboard_tenant
from .user_controller import create_user

urlpatterns = [
    path("onboard/", onboard_tenant, name="onboard_tenant"),
    path("create_user/", create_user, name="create_user"),
]
