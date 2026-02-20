from ..model.students import Students


class StudentRepository:


    @staticmethod
    def create_student(data, tenant_id, user_id):
        student = Students.objects.create(
            tenant_id=tenant_id,
            user_id=user_id,
            no_of_students=data['no_of_students']
        )
        return student