from ninja import NinjaAPI
from .routers import blog_router

api = NinjaAPI(
    urls_namespace='blog',
    title="Blog Management System",
    description=(
        "This API allows users to manage blog posts and comments. "
        "Create, retrieve, and comment on blog posts with ease."
    ),
    version="1.0.0"
)
api.add_router("/blog", blog_router)
