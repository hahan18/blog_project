from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ninja_jwt.exceptions import TokenError, InvalidToken
from .schemas import RegisterSchema, LoginSchema
from .auth import create_jwt
from ninja_jwt.tokens import RefreshToken


def register(request, payload: RegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"error": "Username already exists"}
    if User.objects.filter(email=payload.email).exists():
        return 400, {"error": "Email already registered"}
    User.objects.create_user(username=payload.username, password=payload.password, email=payload.email)
    return 200, {"success": "User registered successfully"}


def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        return 401, {"error": "Invalid credentials"}
    tokens = create_jwt(user)
    return 200, tokens


def refresh_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 401, {"error": "No refresh token provided"}

    _refresh_token = auth_header.split(" ")[1]
    try:
        # Validate the refresh token
        refresh = RefreshToken(_refresh_token)

        # Create a new access token
        new_access_token = str(refresh.access_token)

        # Refresh token rotation
        new_refresh_token = str(refresh)

        return 200, {"access": new_access_token, "refresh": str(new_refresh_token)}
    except (TokenError, InvalidToken):
        return 401, {"error": "Invalid refresh token"}
