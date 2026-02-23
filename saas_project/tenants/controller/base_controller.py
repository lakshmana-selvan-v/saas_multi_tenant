from django.urls import path
from .tenant_controller import onboard_tenant, upgrade_plan_tenant
from .user_controller import create_user, list_users, update_user, delete_user, delete_all_users
from .blog_controller import create_blog, list_blogs, tenant_blogs
from .auth_controller import login

urlpatterns = [
    path("onboard/", onboard_tenant, name="onboard_tenant"),
    path("upgrade/<int:tenant_id>",upgrade_plan_tenant, name="upgrade_plan_tenant" ),
    path("create_user/", create_user, name="create_user"),
    path("list_users/", list_users, name="list_users"),
    path("update_user/<uuid:user_id>/", update_user, name="update_user"),
    path("delete_user/<uuid:user_id>/", delete_user, name="delete_user"),
    path("delete_all_users/", delete_all_users, name="delete_all_users"),
    path("users/<uuid:user_id>/blogs/create/", create_blog, name="create_blog"),
    path("users/<uuid:user_id>/blogs/list/", list_blogs, name="list_blogs"),
    path("blogs/", tenant_blogs, name="tenant_blogs"),
    path("login/", login, name="login"),
]
