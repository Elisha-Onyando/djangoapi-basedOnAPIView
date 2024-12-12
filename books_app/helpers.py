from rest_framework_simplejwt.tokens import RefreshToken


# Helper function to generate JWT tokens
def generate_auth_token(user):
    refresh = RefreshToken.for_user(user)

    refresh['username'] = user.username
    refresh['email'] = user.email

    tokens = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
    return tokens