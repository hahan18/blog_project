from ninja import Router
from .views import create_post, get_posts, add_comment, get_comments_daily_breakdown
from .schemas import PostSchema, CommentSchema, PostResponseSchema

blog_router = Router()


@blog_router.post("/posts", response={200: PostResponseSchema, 400: dict})
def create_post_endpoint(request, payload: PostSchema):
    return create_post(request, payload)


@blog_router.get("/posts", response={200: list[PostResponseSchema]})
def get_posts_endpoint(request):
    return get_posts(request)


@blog_router.post("/posts/{post_id}/comments", response={200: dict, 404: dict})
def add_comment_endpoint(request, post_id: int, payload: CommentSchema):
    return add_comment(request, post_id, payload)


@blog_router.get("/comments-daily-breakdown", response={200: list[dict], 400: dict})
def get_comments_daily_breakdown_endpoint(request, date_from: str, date_to: str):
    return get_comments_daily_breakdown(request, date_from, date_to)
