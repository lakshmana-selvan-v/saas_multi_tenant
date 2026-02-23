from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from ..service.auth_service import AuthService

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    response = AuthService.login(request, data)
    return Response(response, status=status.HTTP_200_OK)

