from ..repository.student_repository import StudentRepository


class StudentService:

    @staticmethod
    def create_student(data, tenant_id, user_id):
        student = StudentRepository.create_student(data, tenant_id, user_id)
        return student