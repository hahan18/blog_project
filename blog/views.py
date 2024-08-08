from datetime import datetime
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from ninja import Router
from user_management.auth import get_user_from_token
from .models import Post, Comment
from .schemas import PostSchema, CommentSchema, PostResponseSchema
from .services import moderate_content
from .tasks import send_auto_reply

router = Router()


@router.post("/posts", response={200: PostResponseSchema, 400: dict})
def create_post(request, payload: PostSchema):
    user = get_user_from_token(request)
    if not user:
        return 401, {"error": "Unauthorized"}

    if moderate_content(payload.content):
        return 400, {"error": "Content is inappropriate"}

    post = Post.objects.create(
        user=user,
        title=payload.title,
        content=payload.content,
        auto_reply_enabled=payload.auto_reply_enabled,
        auto_reply_delay=payload.auto_reply_delay
    )
    return 200, {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat()  # Convert datetime to string
    }


@router.get("/posts", response={200: list[PostResponseSchema]})
def get_posts(request):
    posts = Post.objects.select_related('user').all().order_by('-created_at')
    return 200, [{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat(),  # Convert datetime to string
        "user": post.user.username
    } for post in posts]


@router.post("/posts/{post_id}/comments", response={200: dict, 404: dict})
def add_comment(request, post_id: int, payload: CommentSchema):
    user = get_user_from_token(request)
    if not user:
        return 401, {"error": "Unauthorized"}

    post = get_object_or_404(Post, id=post_id)
    if moderate_content(payload.content):
        Comment.objects.create(post=post, user=user, content=payload.content, is_blocked=True)
        return 200, {"success": False, "error": "Comment is inappropriate and has been blocked"}

    comment = Comment.objects.create(post=post, user=user, content=payload.content)

    if post.auto_reply_enabled:
        send_auto_reply.apply_async(
            args=[comment.id],
            countdown=post.auto_reply_delay * 60
        )

    return 200, {"success": True, "comment_id": comment.id}


@router.get("/comments-daily-breakdown", response={200: list[dict], 400: dict})
def get_comments_daily_breakdown(request, date_from: str, date_to: str):
    user = get_user_from_token(request)
    if not user:
        return 401, {"error": "Unauthorized"}

    # Analytics on comments within a date range
    try:
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        return 400, {"error": "Invalid date format"}

    comments_stats = Comment.objects.filter(
        created_at__date__range=(date_from, date_to)
    ).values('created_at__date').annotate(
        total_comments=Count('id'),
        blocked_comments=Count('id', filter=Q(is_blocked=True))
    )

    daily_stats = [
        {
            "date": stat['created_at__date'].strftime("%Y-%m-%d"),
            "total_comments": stat['total_comments'],
            "blocked_comments": stat['blocked_comments']
        }
        for stat in comments_stats
    ]

    return 200, daily_stats
