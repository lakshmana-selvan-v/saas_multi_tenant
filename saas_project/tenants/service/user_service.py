from ..repository.user_repository import UserRepository


class UserService:
    
    @staticmethod
    def create_user(data, tenant_id):
        user = UserRepository.create_user(data, tenant_id)
        return user
    
    @staticmethod
    def list_users():
        # This will automatically query the correct schema based on the tenant context
        users = UserRepository.list_users()
        return users