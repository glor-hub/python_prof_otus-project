from django.contrib import admin
from django.urls import path, include

app_name = 'vkgroup'
from .views import view

urlpatterns = [
    path('', view, name='test'),
]