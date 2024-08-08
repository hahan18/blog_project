from ninja_jwt.tokens import RefreshToken
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model


def create_jwt(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(' ')[1]  # Extract the token part from the header
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return get_user_model().objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError, get_user_model().DoesNotExist):
        return None
