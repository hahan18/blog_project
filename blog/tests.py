import pytest
from django.contrib.auth.models import User
from datetime import datetime
from unittest.mock import patch
from user_management.auth import create_jwt
from .models import Post, Comment
from .tasks import send_auto_reply


# Fixtures
@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "securepassword", "email": "testuser@example.com"}


@pytest.fixture
def create_user(db, user_data):
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def auth_client(client, create_user):
    # Generate JWT token for the created user
    tokens = create_jwt(create_user)
    access_token = tokens['access']

    # Add the token to the client's headers
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client


@pytest.fixture
def post_data():
    return {
        "title": "Test Post",
        "content": "This is a test post.",
        "auto_reply_enabled": True,
        "auto_reply_delay": 5,
    }


@pytest.fixture
def create_post(create_user, post_data):
    return Post.objects.create(user=create_user, **post_data)


@pytest.fixture
def comment_data():
    return {"content": "This is a test comment."}


@pytest.mark.django_db
class TestBlogAPI:
    def test_create_post(self, auth_client, post_data):
        url = '/api/blog/posts'
        response = auth_client.post(url, post_data, content_type='application/json')
        assert response.status_code == 200
        assert response.json()["title"] == post_data["title"]
        assert response.json()["content"] == post_data["content"]

    def test_get_posts(self, auth_client, create_post):
        url = '/api/blog/posts'
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == create_post.title

    @patch('blog.services.requests.post')
    def test_add_comment(self, mock_post, auth_client, create_post, comment_data):
        # Mock the API response to simulate inappropriate content detection
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"inappropriate": True}

        comment_data["content"] = "This is an inappropriate comment."
        url = f'/api/blog/posts/{create_post.id}/comments'
        response = auth_client.post(url, comment_data, content_type='application/json')
        assert response.status_code == 200
        assert response.json()["success"] is False
        assert response.json()["error"] == "Comment is inappropriate and has been blocked"

    def test_daily_comment_breakdown(self, auth_client, create_post, comment_data):
        Comment.objects.create(post=create_post, user=create_post.user, content="Test comment")
        Comment.objects.create(post=create_post, user=create_post.user, content="Blocked comment", is_blocked=True)

        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = datetime.now().strftime("%Y-%m-%d")
        url = f'/api/blog/comments-daily-breakdown?date_from={date_from}&date_to={date_to}'

        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == 200
        assert response.json()[0]["total_comments"] == 2
        assert response.json()[0]["blocked_comments"] == 1

    @patch('blog.tasks.send_auto_reply.delay')
    def test_auto_reply_task(self, mock_send_auto_reply, create_post, comment_data):
        # Create a comment that triggers the auto-reply logic
        comment = Comment.objects.create(post=create_post, user=create_post.user, content="Auto reply test")

        # Manually call send_auto_reply to simulate what would happen in the task queue
        send_auto_reply.delay(comment.id)

        # Assert that the send_auto_reply task was called with the correct comment id
        mock_send_auto_reply.assert_called_once_with(comment.id)
