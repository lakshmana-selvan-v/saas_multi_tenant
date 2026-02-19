from ..repository.user_repository import UserRepository


class UserService:
    
    @staticmethod
    def create_user(data, tenant_id):
        user = UserRepository.create_user(data, tenant_id)
        return user
    
    @staticmethod
    def list_users():
        users = UserRepository.list_users()
        return users
    
    @staticmethod
    def delete_user(user_id):
        user = UserRepository.delete_user(user_id)
        return user
    
    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.update_particular_user(user_id, data)
        if not user:
            raise Exception("User not found")
        return user

    @staticmethod
    def delete_all_users(tenant_id):
        users = UserRepository.delete_all_users(tenant_id)
        return users