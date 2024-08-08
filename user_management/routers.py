from ninja import Router
from .views import register, login, refresh_token
from .schemas import RegisterSchema, LoginSchema, TokenSchema

user_router = Router()


@user_router.post("/register", response={200: dict, 400: dict})
def register_endpoint(request, payload: RegisterSchema):
    return register(request, payload)


@user_router.post("/login", response={200: TokenSchema, 401: dict})
def login_endpoint(request, payload: LoginSchema):
    return login(request, payload)


@user_router.post("/token/refresh", response={200: TokenSchema, 401: dict})
def refresh_token_endpoint(request):
    return refresh_token(request)
