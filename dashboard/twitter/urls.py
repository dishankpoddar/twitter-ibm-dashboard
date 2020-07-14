from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.bar, name='index'),
    path('bar/', views.bar, name='bar'),
    path('line/', views.line, name='line'),
    path('pie/', views.pie, name='pie'),
    path('load/',views.populateTweets),
    path('delete/',views.deleteTweets),
]
