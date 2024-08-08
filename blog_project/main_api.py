from ninja import NinjaAPI
from blog.routers import blog_router
from user_management.routers import user_router

main_api = NinjaAPI(
    title="Unified API",
    description=(
        "This API provides endpoints for managing blog posts and comments, "
        "as well as user registration and authentication."
    ),
    version="1.0.0"
)

main_api.add_router("/blog", blog_router, tags=["Blog Management"])
main_api.add_router("/users", user_router, tags=["User Management"])
