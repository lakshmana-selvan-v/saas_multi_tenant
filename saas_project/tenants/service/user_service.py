from ..repository.user_repository import UserRepository


class UserService:
    
    @staticmethod
    def create_user(data, tenant_id):
        user = UserRepository.create_user(data, tenant_id)
        return user