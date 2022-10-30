from django.shortcuts import render

from .vkapi_services import main
import logging
logger = logging.getLogger(__name__)

def view(request):
    main.main_run()
    context = {
        'title': 'Uraaa'
    }
    return render(request, 'home.html', context)
