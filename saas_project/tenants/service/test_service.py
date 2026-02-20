from ..repository.test_repository import TestRepository


class TestService:

    @staticmethod
    def scenario1_get_all_users():
        users = TestRepository.scenario1_get_all_users()
        return [{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in users]

    @staticmethod
    def scenario_2_3_users_by_tenant(tenant_id):
        users = TestRepository.scenario_2_3_users_by_tenant(tenant_id)
        return [{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in users]

    @staticmethod
    def scenario_4_get_all_students():
        students = TestRepository.scenario_4_get_all_students()
        return [{"id": student.id, "no_of_students": student.no_of_students, "tenant_id": student.tenant_id} for student in students]

    @staticmethod
    def scenario_5_get_students_by_tenant(tenant_id):
        students = TestRepository.scenario_5_get_students_by_tenant(tenant_id)
        return [{"id": student.id, "no_of_students": student.no_of_students, "tenant_id": student.tenant_id} for student in students]

    @staticmethod
    def scenario_6_get_user_ids():
        user_ids = TestRepository.scenario_6_get_user_ids()
        return [{"id": id} for id in user_ids]

    @staticmethod
    def scenario_7_get_user_ids(tenant_id):
        user_ids = TestRepository.scenario_7_get_user_ids(tenant_id)
        return [{"id": id} for id in user_ids]

    @staticmethod
    def scenario_9_get_user_ids():
        user_ids = TestRepository.scenario_9_get_user_ids()
        return [{"id": id} for id in user_ids]

    @staticmethod
    def scenario_9_get_user_ids_by_tenant(tenant_id):
        user_ids = TestRepository.scenario_9_get_user_ids_by_tenant(tenant_id)
        return [{"id": id} for id in user_ids]

    @staticmethod
    def scenario_10_users_from_students():
        user_ids = TestRepository.scenario_10_users_from_students()
        return [{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in user_ids]