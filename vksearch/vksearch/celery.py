# -*- coding: utf-8 -*-
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vksearch.vksearch.settings')

celery_app = Celery('vksearch')

celery_app.conf.timezone = 'UTC'
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
