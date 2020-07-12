from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from django.views.generic import (View,TemplateView,CreateView, DeleteView, DetailView, 
                                    ListView,UpdateView,FormView)
from django.db import transaction
from django.db.models import Avg, Count, F, Aggregate
from django.conf import settings 
from .models import Tweets

import csv

def index(request):
    context = {
        'india_map': settings.MEDIA_ROOT+"/india.svg"
    }
    return render(request, 'twitter/index.html',context)

def populateTweets(request):
    
    csvFile = 'twitter/tweets_annotated_lite.csv'
    
    try :
        with open(csvFile) as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                print(row['index'],end=' ')
                print(row['date'],end=' ')
                print(row['time'],end=' ')
                print(row['username'],end=' ')
                print(row['name'],end=' ')
                print(row['tweet'],end=' ')
                print(row['geo'],end=' ')
                print(row['Positive'],end=' ')
                print(row['Happy'],end=' ')
                print(row['Relief'],end=' ')
                print(row['Neutral'],end=' ')
                print(row['Anxious'],end=' ')
                print(row['Sad'],end=' ')
                print(row['Negative'],end=' ')

                p = Tweets(index = row['index'],
                            date = row['date'],
                            time = row['time'],
                            username = row['username'],
                            name = row['name'],
                            tweet = row['tweet'],
                            geo = row['geo'],
                            positive = (True if row['Positive']=='1' else False),
                            happy = (True if row['Happy']=='1' else False),
                            relief = (True if row['Relief']=='1' else False),
                            neutral = (True if row['Neutral']=='1' else False),
                            anxious = (True if row['Anxious']=='1' else False),
                            sad = (True if row['Sad']=='1' else False),
                            negative = (True if row['Negative']=='1' else False))
                p.save()

    except Exception as e:
        print(e)
        # log Error

    return HttpResponse("Ho gayaaaaa")
    