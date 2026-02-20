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
    user_data = [{"id": user.id, "email": user.email, "name": user.name, "age": user.age} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_user(request, user_id):
    data = request.data
    try:
        user = UserService.update_user(user_id, data)
        return Response(
            {"message": "User updated successfully", "user_id": user.id},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["DELETE"])
def delete_user(request, user_id):
    success = UserService.delete_user(user_id)
    if success:
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_all_users(request):
    tenant_id = get_current_tenant_id()
    success = UserService.delete_all_users(tenant_id)
    if success:
        return Response({"message": "All users deleted successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to delete all users"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)