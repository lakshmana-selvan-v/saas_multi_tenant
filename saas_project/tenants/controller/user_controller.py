from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.user_service import UserService
from ..core.context_variable import get_current_tenant_id

@api_view(["POST"])
def create_user(request):
    data = request.data
    tenant_id = get_current_tenant_id()
    user = UserService.create_user(data, tenant_id=tenant_id)
    return Response(
        {"message": "User created successfully", "user_id": user.id},
        status=status.HTTP_201_CREATED,
    )
    
@api_view(["GET"])
def list_users(request):
    users = UserService.list_users()
    user_data = [{"id": user.id, "email": user.email, "role": user.role} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)