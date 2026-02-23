from django.contrib.auth import authenticate
from ..security.custom_jwt import get_tokens_for_user


class AuthService:

    @staticmethod
    def login(request, data):
        try:
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request=request, email=email, password=password)
            if not user:
                return {'error': 'Invalid credentials'}
            tokens = get_tokens_for_user(user)
            return {'message': 'Login successful', 'tokens': tokens}
        except Exception as e:
            return {'error': str(e)}

