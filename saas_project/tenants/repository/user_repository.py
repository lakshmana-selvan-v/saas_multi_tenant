from ..model.users import User

class UserRepository:
    
    @staticmethod
    def create_user(data, tenant_id):
        user = User.objects.create(
            tenant_id =tenant_id,
            email =data['email'],
            role =data['role']
        )
        return user
    
    @staticmethod
    def list_users():
        users = User.objects.all()
        return users