from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.test_service import TestService


@api_view(["GET"])
def test_scenario1(request):
    users = TestService.scenario1_get_all_users()
    return Response(
        {"message": "Test scenario 1 completed successfully", "users": users},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario2(request, tenant_id):
    users = TestService.scenario_2_3_users_by_tenant(tenant_id)
    return Response(
        {"message": "Test scenario 2 completed successfully", "users": users},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario4(request):
    students = TestService.scenario_4_get_all_students()
    return Response(
        {"message": "Test scenario 4 completed successfully", "students": students},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario5(request, tenant_id):
    students = TestService.scenario_5_get_students_by_tenant(tenant_id)
    return Response(
        {"message": "Test scenario 5 completed successfully", "students": students},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario6(request):
    ids = TestService.scenario_6_get_user_ids()
    return Response(
        {"message": "Test scenario 6 completed successfully", "ids": ids},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def test_scenario7(request, tenant_id):
    user_ids = TestService.scenario_7_get_user_ids(tenant_id)
    return Response(
        {"message": "Test scenario 7 completed successfully", "user_ids": user_ids},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario8(request):
    ids = TestService.scenario_9_get_user_ids()
    return Response(
        {"message": "Test scenario 8 completed successfully", "ids": ids},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario9(request, tenant_id):
    user_ids = TestService.scenario_9_get_user_ids_by_tenant(tenant_id)
    return Response(
        {"message": "Test scenario 9 completed successfully", "user_ids": user_ids},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def test_scenario10(request):
    ids = TestService.scenario_10_users_from_students()
    return Response(
        {"message": "Test scenario 10 completed successfully", "ids": ids},
        status=status.HTTP_200_OK,
    )