from django.contrib import admin
from django.urls import path, include

app_name = 'vkgroup'
from .views import  search_profile, search_result
urlpatterns = [
    path('', search_profile, name='search'),
    path('result/', search_result, name='result'),
]
