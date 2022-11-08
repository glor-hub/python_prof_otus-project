from django.contrib import admin
from django.urls import path, include

app_name = 'vkgroup'
from .views import  test_search_profile, test_search_result
urlpatterns = [
    path('', test_search_profile, name='search'),
    path('result/', test_search_result, name='result'),
]
