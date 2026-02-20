from ..model.users import User
from ..model.students import Students

class TestRepository:

    @staticmethod
    def scenario1_get_all_users():
        users = User.objects.all()
        return users

    @staticmethod
    def scenario_2_3_users_by_tenant(tenant_id):
        users = User.objects.filter(tenant_id=tenant_id)
        return users

    @staticmethod
    def scenario_4_get_all_students():
        students = Students.objects.all()
        return students

    @staticmethod
    def scenario_5_get_students_by_tenant(tenant_id):
        students = Students.objects.filter(tenant_id=tenant_id)
        return students
    
    @staticmethod
    def scenario_6_get_user_ids():
        user_ids = User.objects.values_list('id', flat=True)
        return list(user_ids)
    
    @staticmethod
    def scenario_7_get_user_ids(tenant_id):
        user_ids = User.objects.filter(tenant_id=tenant_id).values_list('id', flat=True)
        return list(user_ids)

    @staticmethod
    def scenario_9_get_user_ids():
        user_ids = Students.objects.values_list('user_id', flat=True).distinct()
        return list(user_ids)

    @staticmethod
    def scenario_9_get_user_ids_by_tenant(tenant_id):
        user_ids  = Students.objects.filter(tenant_id=tenant_id).values_list('user_id', flat=True).distinct()
        return list(user_ids)

    @staticmethod
    def scenario_10_users_from_students():
        students_user_ids = Students.objects.values_list('user_id', flat=True).distinct()
        users = User.objects.filter(id__in=students_user_ids)
        return list(users)  