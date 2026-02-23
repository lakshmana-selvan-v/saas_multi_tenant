from rest_framework.exceptions import PermissionDenied
from ..core.context_variable import get_current_tenant_id

def validate_user(request):

    user = request.user

    if not user.is_authenticated:
        raise PermissionDenied("User is not authenticated")

    current_tenant_id = get_current_tenant_id()

    if str(user.tenant_id) != str(current_tenant_id):
        raise PermissionDenied("User is not authorized to access this resource")
    
    return True