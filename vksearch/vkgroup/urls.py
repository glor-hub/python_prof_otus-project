from django.urls import path

app_name = "vkgroup"
from .views import communities_view

urlpatterns = [
    path("", communities_view, name="search"),
]
