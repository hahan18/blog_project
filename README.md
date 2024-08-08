# Unified API for Blog and User Management

## Description

The Unified API is a centralized platform designed to manage blog posts and comments efficiently while offering
comprehensive user registration and authentication functionalities. This Django-based application simplifies handling
blog interactions and user management with robust features and secure practices using Django Ninja for API creation.

## Key Features

- **User Registration and Authentication**: Utilizes Django's robust user management framework enhanced with JWT for
  secure token handling.
- **Blog Management**: Enables users to create and manage comments on blog posts.
- **Comment Analytics**: Provides daily breakdowns of comments to assess user engagement and content interaction.
- **Asynchronous Task Processing**: Leverages Celery with Redis for handling background tasks such as sending
  notifications or processing data asynchronously.

## Technology Stack

- **Django & Django Ninja**: For constructing a secure and scalable backend.
- **PostgreSQL**: As the primary data storage solution.
- **Docker & Docker Compose**: For containerization and easy deployment.
- **Celery & Redis**: For managing asynchronous tasks and message brokering.

## Installation Guide

### Prerequisites

Ensure you have Docker and Docker Compose installed on your machine. You can download them from:

- Docker: [Get Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Docker Compose](https://docs.docker.com/compose/install/)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hahan18/blog_project.git  
   cd blog_project
   ```

2. **Start the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
   The application will be accessible at `http://localhost:8000`.

### API Endpoints

**Blog Management**

- `POST /api/blog/posts`: Create a new blog post.
- `GET /api/blog/posts`: Retrieve all blog posts.
- `POST /api/blog/posts/{post_id}/comments`: Add a comment to a post.
- `GET /api/blog/comments-daily-breakdown`: Get daily analytics for comments.

**User Management**

- `POST /api/users/register`: Register a new user.
- `POST /api/users/login`: Authenticate a user and obtain tokens.
- `POST /api/users/token/refresh`: Refresh the authentication token.

## Running Tests

Execute automated tests with coverage by running:

```bash
docker-compose exec web coverage run -m pytest
docker-compose exec web coverage report -m
```

## Authors

- **Oleksandr Khakhanovskyi** - "Blog project"

