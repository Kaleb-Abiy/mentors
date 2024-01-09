# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Replace 'your_project' with your Django project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentors.settings')

# Replace 'your_project' with your Django project name
app = Celery('mentors')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
