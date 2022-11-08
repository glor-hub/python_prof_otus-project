from django.shortcuts import render

import logging

from . import tasks
# from tasks import create_task
from vksearch import celery_app

logger = logging.getLogger(__name__)

def search_profile(request):
    # to do form
    context = {
        'title': 'Search Profile'
    }
    return render(request, 'profile.html', context)

def search_result(request):
    # task = create_task.delay()
    # task_id = task.id
    # task = celery_app.AsyncResult(task_id)
    # # task_status = str(task.status)
    # task_status=True
    # context = {
    #     'title': 'Search Result',
    #     'task_status': task_status,
    #     # 'task_id': task_id
    # def view(request):
        # main.main_run()
    task = tasks.create_task.delay()
    task_id = task.id
    task = celery_app.AsyncResult(task_id)
    status = task.status
    context = {
        'title': 'Uraaa'
    }
    return render(request, 'result.html', context)
