from django.shortcuts import render

import logging

from .tasks import create_task
from vksearch import celery_app

logger = logging.getLogger(__name__)

def view(request):
    task=create_task.delay()
    task_id=task.id
    task = celery_app.AsyncResult(task_id)
    status = task.status
    context = {
        'title': 'Uraaa'
    }
    return render(request, 'home.html', context)
