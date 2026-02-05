from django.urls import path
from .tenant_controller import onboard_tenant, upgrade_plan_tenant
from .user_controller import create_user

urlpatterns = [
    path("onboard/", onboard_tenant, name="onboard_tenant"),
    path("upgrade/<int:tenant_id>",upgrade_plan_tenant, name="upgrade_plan_tenant" ),
    path("create_user/", create_user, name="create_user"),
]
