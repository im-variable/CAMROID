from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myspace', views.myspace, name='myspace'),
    path('category', views.category, name='category'),
    path('aboutus', views.AboutUs.as_view(), name='aboutus'),
    url(r'^getSuggestion/$', views.getSuggestion, name='getSuggestion'),
    path('single/<str:img_name>', views.Single.as_view(), name='single-val'),
    path('single', views.Single.as_view(), name='single'),
    # url(r'^aboutus/$', views.AboutUs.as_view(), name='aboutus'),

]
