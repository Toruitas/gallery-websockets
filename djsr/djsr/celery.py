import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsr.settings')

app = Celery('djsr')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery worker --app djsr.celery.app --loglevel info