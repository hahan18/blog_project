from celery import shared_task
from .models import Comment


@shared_task
def send_auto_reply(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        post = comment.post

        # Check if the comment still needs a reply (not replied or blocked)
        if not Comment.objects.filter(
                post=post,
                content__startswith="Auto-reply to comment",
                created_at__gt=comment.created_at,
                user=post.user
        ).exists() and not comment.is_blocked:
            reply_content = f"Auto-reply to comment: {comment.content}"
            Comment.objects.create(post=post, user=post.user, content=reply_content)
    except Comment.DoesNotExist:
        # Handle case where comment does not exist
        pass
