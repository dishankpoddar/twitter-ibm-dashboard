from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from django.views.generic import (View,TemplateView,CreateView, DeleteView, DetailView, 
                                    ListView,UpdateView,FormView)
from django.db import transaction
from django.db.models import Avg, Count, F, Aggregate
from django.conf import settings 
from .models import Tweets

import csv

def index(request):
    return render(request, 'twitter/index2.html')

def line(request):
    return render(request, 'twitter/line.html')

def pie(request):
    return render(request, 'twitter/pie.html')

def deleteTweets(request):
    # batch = Tweets.objects.last().batch
    # Tweets.objects.filter(batch=batch).delete()
    return HttpResponse("This script is commented in order to avoid accidental deletes")

def populateTweets(request):
    
    batch = Tweets.objects.last().batch+1
    print(batch)
    csvFile = 'twitter/tweets_annotated_lite.csv'
    numberOfRows = 0

    with open(csvFile, encoding='utf8') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            try :
                numberOfRows+=1
                p = Tweets(index = row['index'],
                            batch = batch,
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
    
    numberOfTweetsLoaded = Tweets.objects.filter(batch=batch).count()

    return HttpResponse("Batch Number : "+str(batch)+". <br><br>Number of Tweets added successfully :  "+str(numberOfTweetsLoaded)+"/"+str(numberOfRows)+". <br><br>CSV File fetched : '"+str(csvFile.name)+"'")
