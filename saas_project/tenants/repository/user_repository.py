from ..model.users import User

class UserRepository:
    
    @staticmethod
    def create_user(data, tenant_id):
        user = User.objects.create(
            tenant_id =tenant_id,
            email =data['email'],
            name =data['name'],
            age =data['age']
        )
        return user
    
    @staticmethod
    def update_particular_user(user_id, data):
        try:
            user = User.objects.get(id=user_id)
            user.email = data.get("email", user.email)
            user.name = data.get("name", user.name)
            user.age = data.get("age", user.age)
            user.save()
            return user
        except User.DoesNotExist:
            return None
        
    @staticmethod
    def delete_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
    
    @staticmethod
    def list_users():
        users = User.objects.all()
        return users

    @staticmethod
    def delete_all_users():
        users = User.objects.all()
        for user in users:
            user.delete()
        return True