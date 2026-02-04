from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.user_service import UserService


@api_view(["POST"])
def create_user(request):
    data = request.data
    tenant_id = request.headers["X-Tenant-ID"]
    user = UserService.create_user(data, tenant_id=tenant_id)
    return Response(
        {"message": "User created successfully", "user_id": user.id},
        status=status.HTTP_201_CREATED,
    )