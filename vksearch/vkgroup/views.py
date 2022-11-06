from django.shortcuts import render

import logging

from .tasks import create_task
from vksearch import celery_app

logger = logging.getLogger(__name__)

def search_profile(request):
    # to do form
    context = {
        'title': 'Search Profile'
    }
    return render(request, 'profile.html', context)

def search_result(request):
    task = create_task.delay()
    task_id = task.id
    task = celery_app.AsyncResult(task_id)
    task_status = str(task.status)
    context = {
        'title': 'Search Result',
    }
    return render(request, 'result.html', task_status, task_id, context)
