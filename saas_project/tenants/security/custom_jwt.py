from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)



    refresh['email'] = user.email
    refresh['full_name'] = user.full_name
    refresh['tenant_id'] = str(user.tenant_id)

    access = refresh.access_token
    access['email'] = user.email
    access['full_name'] = user.full_name
    access['tenant_id'] = str(user.tenant_id)

    return {
        'refresh': str(refresh),
        'access': str(access),
    }

