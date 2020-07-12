from django.urls import path,include
from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('load/',views.populateTweets),
    path('delete/',views.deleteTweets)
]
