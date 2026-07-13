from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


def get_auth_response(user):
    refresh = RefreshToken.for_user(user)

    return {
        "user": UserSerializer(user).data,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }