from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

app = Celery('blog_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
