from django.urls import path,include
from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('line/', views.line, name='line'),
    path('pie/', views.pie, name='pie'),
    path('load/',views.populateTweets),
    path('delete/',views.deleteTweets)
]
