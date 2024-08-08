from ninja import NinjaAPI
from .routers import user_router

api = NinjaAPI(
    urls_namespace='user_management',
    title="User Management Service",
    description=(
        "This service provides endpoints for user account management, "
        "including registration and authentication. "
        "It uses JWT for secure token-based authentication."
    ),
    version="1.0.0"
)
api.add_router("/users", user_router)
