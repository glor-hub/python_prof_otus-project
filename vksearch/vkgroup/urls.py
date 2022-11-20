from django.contrib import admin
from django.urls import path, include

app_name = 'vkgroup'
from .views import communities_view
urlpatterns = [
    path('', communities_view, name='search'),
]
