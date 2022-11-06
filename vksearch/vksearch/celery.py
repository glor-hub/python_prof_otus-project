# -*- coding: utf-8 -*-
# from __future__ import absolute_import
import os

# import export as export
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vksearch.settings')
#: Set default configuration module name
# os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')
# export DJANGO_SETTINGS_MODULE="vksearch.settings"

settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vksearch.settings")


celery_app = Celery('vksearch',backend='rpc://')
# celery_app.config_from_envvar('CELERY_CONFIG_MODULE')

# celery_app.conf.timezone = 'UTC'
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
# celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
celery_app.autodiscover_tasks()

