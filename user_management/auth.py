from ninja_jwt.tokens import RefreshToken


def create_jwt(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}
