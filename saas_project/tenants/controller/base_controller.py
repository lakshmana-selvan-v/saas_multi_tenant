from django.urls import path
from .tenant_controller import onboard_tenant, upgrade_plan_tenant
from .user_controller import create_user, list_users, update_user, delete_user, delete_all_users
from .blog_controller import create_blog, list_blogs, tenant_blogs
from .student_controller import create_student
from .test_controller import test_scenario1, test_scenario2, test_scenario4, test_scenario5, test_scenario6, test_scenario7, test_scenario8, test_scenario9, test_scenario10

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
    path("users/<uuid:user_id>/students/create/", create_student, name="create_student"),
    path("test/scenario1/", test_scenario1, name="test_scenario1"),
    path("test/scenario2/<uuid:tenant_id>/", test_scenario2, name="test_scenario2"),
    path("test/scenario4/", test_scenario4, name="test_scenario4"),
    path("test/scenario5/<uuid:tenant_id>/", test_scenario5, name="test_scenario5"),
    path("test/scenario6/", test_scenario6, name="test_scenario6"),
    path("test/scenario7/<uuid:tenant_id>/", test_scenario7, name="test_scenario7"),
    path("test/scenario8/", test_scenario8, name="test_scenario8"),
    path("test/scenario9/<uuid:tenant_id>/", test_scenario9, name="test_scenario9"),
    path("test/scenario10/", test_scenario10, name="test_scenario10"),
]
