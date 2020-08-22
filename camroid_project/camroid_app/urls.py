from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myspace', views.myspace, name='myspace'),
    path('category', views.category, name='category'),
    url(r'^getSuggestion/$', views.getSuggestion, name='getSuggestion')
]