from django.shortcuts import render

from .vkapi_services import main


def view(request):
    main.main_run()
    context = {
        'title': 'Uraaa'
    }
    return render(request, 'home.html', context)
