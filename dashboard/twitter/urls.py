from django.urls import path,include
from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('line/', views.index, name='line'),
    path('pie/', views.index, name='pie'),
    path('load/',views.populateTweets),
    path('delete/',views.deleteTweets)
]
