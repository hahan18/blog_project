from ninja import Schema


class PostSchema(Schema):
    title: str
    content: str
    auto_reply_enabled: bool = False  # Default to False if not provided
    auto_reply_delay: int = 0  # Default delay time in minutes


class CommentSchema(Schema):
    content: str


class PostResponseSchema(Schema):
    id: int
    title: str
    content: str
    created_at: str
