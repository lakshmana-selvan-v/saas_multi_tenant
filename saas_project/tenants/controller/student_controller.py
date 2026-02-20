from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.student_service import StudentService
from ..core.context_variable import get_current_tenant_id


@api_view(["POST"])
def create_student(request, user_id):
    data = request.data
    tenant_id = get_current_tenant_id()
    student = StudentService.create_student(data, tenant_id, user_id)
    return Response(
        {"message": "Student created successfully", "student_id": student.id},
        status=status.HTTP_201_CREATED,
    )