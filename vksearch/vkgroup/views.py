from django.shortcuts import render

import logging

from .tasks import test_create_task

from vksearch import celery_app

logger = logging.getLogger(__name__)

def test_search_profile(request):
    # to do form
    context = {
        'title': 'Search Profile'
    }
    return render(request, 'profile.html', context)

def test_search_result(request):
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
    task = test_create_task.delay()
    t_id = task.id
    task = celery_app.AsyncResult(t_id)
    t_status = task.status
    context = {
        'title': 'Uraaa',
        'task_id': t_id,
        'task_status': t_status
    }
    return render(request, 'result.html', context)

def search_profile(request):
    # to do form
    context = {
        'title': 'Search Profile'
    }
    return render(request, 'profile.html', context)

def search_result(request):
    # to do
    context = {
        'title': 'Search Profile'
    }
    return render(request, 'profile.html', context)