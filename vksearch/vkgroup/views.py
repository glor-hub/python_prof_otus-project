from django.shortcuts import render

# from .vkapi_services import main
import logging

from .tasks import create_task

logger = logging.getLogger(__name__)

def view(request):
    # main.main_run()
    create_task()
    context = {
        'title': 'Uraaa'
    }
    return render(request, 'home.html', context)
