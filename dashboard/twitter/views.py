from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from django.views.generic import (View,TemplateView,CreateView, DeleteView, DetailView, 
                                    ListView,UpdateView,FormView)
from django.db import transaction
from django.db.models import Avg, Count, F, Aggregate,Q
from django.conf import settings 
from .models import Tweets

from functools import reduce
import operator

import time
from datetime import date,timedelta
from datetime import datetime

from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt

import csv

def word_count(my_string,stopwords):
    counts = dict()
    words = my_string.split()
    for word in words:
        if word not in stopwords:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return counts

def bar(request):
    start = time.time()
    all_tweets = Tweets.objects.all()
    filter_date = date.today()
    if(request.method == 'POST'):
        print('yay')
    tweet_cloud = ""
    for tweet in all_tweets:
        tweet_cloud += " "+tweet.tweet
    stopwords = STOPWORDS|set(['covid','corona','lockdown','quarantine'])|set(["<NATURE>","<FOOD>","<SPACE-TIME>","<ACTIVITIES>","<OBJECTS>","<SYMBOLS>","<FLAGS>","<PERSON>","<HAPPY>","<LAUGH>","<LOVE>","<SARCASM>","<DOUBT>","<UNWELL>","<SAD>","<PISSED>","<SLEEPY>","<NEUTRAL>","<SHOCK>","<PATRIOT>"]) 
    
    
    wordcloud = WordCloud(width = 720, height = 360, 
                background_color ='#010232', 
                stopwords = stopwords, 
                min_font_size = 10).generate(tweet_cloud) 
    plt.figure(figsize = (16, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.savefig('./twitter/static/twitter/word.png')

    top_5 = word_count(tweet_cloud,stopwords)[:5]
    top_5 = [[top[0]] for top in top_5]
    for top in top_5:
        top_tweet = Tweets.objects.filter(tweet__contains=top[0])
        neg_top_5 = top_tweet.filter(Q(negative=True)|Q(sad=True)|Q(anxious=True)).count()
        pos_top_5 = top_tweet.filter(Q(positive=True)|Q(happy=True)|Q(relief=True)).count()
        top.extend([neg_top_5,pos_top_5])
        print(top)
    
    filter_date = datetime.strptime("2020-06-12", "%Y-%m-%d").date()
    #print(Tweets.objects.filter(date=filter_date))

    pos_neg_filter_date = filter_date
    pos_neg_days = []
    for i in range(7):
        pos_neg_days.append([pos_neg_filter_date])
        date_tweet = Tweets.objects.filter(date=pos_neg_filter_date)
        neg_date_tweet = date_tweet.filter(Q(negative=True)|Q(sad=True)|Q(anxious=True)).count()
        pos_date_tweet = date_tweet.filter(Q(positive=True)|Q(happy=True)|Q(relief=True)).count()
        try:
            neg_perc = neg_date_tweet/(neg_date_tweet+pos_date_tweet)
            pos_perc = pos_date_tweet/(neg_date_tweet+pos_date_tweet)
        except:
            neg_perc = 0
            pos_perc = 0
        pos_neg_days[i].extend([neg_perc,pos_perc])
        pos_neg_filter_date -= timedelta(days=1)
        print(pos_neg_days[i])

    emotion_filter_date = filter_date
    emotion_days = []
    for i in range(7):
        emotion_days.append([emotion_filter_date])
        date_tweet = Tweets.objects.filter(date=emotion_filter_date)
        neg_date_tweet = date_tweet.filter(Q(negative=True)).count()
        sad_date_tweet = date_tweet.filter(Q(sad=True)).count()
        anx_date_tweet = date_tweet.filter(Q(anxious=True)).count()
        neu_date_tweet = date_tweet.filter(Q(neutral=True)).count()
        rel_date_tweet = date_tweet.filter(Q(relief=True)).count()
        hap_date_tweet = date_tweet.filter(Q(happy=True)).count()
        pos_date_tweet = date_tweet.filter(Q(positive=True)).count()
        emotion_days[i].extend([neg_date_tweet,sad_date_tweet,anx_date_tweet,neu_date_tweet,rel_date_tweet,hap_date_tweet,pos_date_tweet])
        emotion_filter_date -= timedelta(days=1)
        print(emotion_days[i])
    end = time.time()
	



    context = {
        'bar' : True,
        'wordcloud' :settings.MEDIA_ROOT+"/word.png"
    }
    # return HttpResponse(f"Runtime of the query is {end - start}")
    return render(request, 'twitter/bar.html',context)

def line(request):
    context = {
        'line' : True
    }
    return render(request, 'twitter/line.html',context)

def pie(request):
    context = {
        'pie' : True
    }
    return render(request, 'twitter/pie.html',context)

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
