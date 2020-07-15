from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from django.views.generic import (View,TemplateView,CreateView, DeleteView, DetailView, 
                                    ListView,UpdateView,FormView)
from django.db import transaction
from django.db.models import Avg, Count, F, Aggregate,Q
from django.conf import settings 
from .models import Tweets
from django.http import JsonResponse
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

filters_Default = {'date':date.today(),'loc':None,'content':None}

def bar(request):
    start = time.time()
    get_tweets = Tweets.objects.all()
    #filters_date = date.today()
    filters_date = datetime.strptime("July 14, 2020", "%B %d, %Y").date() 
    filters_content = filters_Default['content']
    filters_loc = filters_Default['loc']

    max_color = "blue"
    
    if(request.method == 'POST'):
        if(request.POST['reset']=='false'):
            filters_date = request.POST['date']
            try:
                filters_date = datetime.strptime(filters_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date() 
            except:
                filters_date = datetime.strptime(filters_date, "%B %d, %Y").date() 
            filters_content = request.POST['content']
            filters_loc = request.POST['loc']
            if(filters_content!="None"):
                get_tweets = get_tweets.filter(tweet__contains=filters_content)
            if(filters_loc!="None"):
              get_tweets = get_tweets.filter(geo=filters_loc)


            
        elif(request.POST['reset']=='true'):
            filters_date = filters_Default['date']
            filters_content = filters_Default['content']
            filters_loc = filters_Default['loc']
    print(get_tweets.filter(date=filters_date).count(),type(filters_content),filters_loc)
    tweet_cloud = ""
    for tweet in get_tweets:
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
    top_5 = [top[0] for top in top_5]
    neg_top_5,pos_top_5=[],[]
    for top in top_5:
        top_tweet = get_tweets.filter(tweet__contains=top[0])
        neg_top_5.append(top_tweet.filter(Q(negative=True)|Q(sad=True)|Q(anxious=True)).count())
        pos_top_5.append(top_tweet.filter(Q(positive=True)|Q(happy=True)|Q(relief=True)).count())
        # print(top)
    top_5 = {'terms':top_5,'positive':pos_top_5,'negative':neg_top_5}

    #print(top_5)

    #given_date = "Fri Jun 12 2020 18:11:17 GMT+0530 (India Standard Time)"
    #filters_date = datetime.strptime(given_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date()      
    #print(get_tweets.filter(date=filters_date))

    pos_neg_filters_date = filters_date
    pos_neg_dates = []
    neg_perc = []
    pos_perc = []
    for _ in range(7):
        pos_neg_dates.append(pos_neg_filters_date.day)
        date_tweet = get_tweets.filter(date=pos_neg_filters_date)
        neg_date_tweet = date_tweet.filter(Q(negative=True)|Q(sad=True)|Q(anxious=True)).count()
        pos_date_tweet = date_tweet.filter(Q(positive=True)|Q(happy=True)|Q(relief=True)).count()
        try:
            neg_perc.append(neg_date_tweet/(neg_date_tweet+pos_date_tweet))
            pos_perc.append(pos_date_tweet/(neg_date_tweet+pos_date_tweet))
        except:
            neg_perc.append(0)
            pos_perc.append(0)
        pos_neg_filters_date -= timedelta(days=1)
        # print(pos_neg_days[i])
    pos_neg = {'dates':pos_neg_dates[::-1],'positive':pos_perc[::-1],'negative':neg_perc[::-1]}
    #print(pos_neg)

    emotion_filters_date = filters_date
    emotion_dates = []
    sad_date_tweet,anx_date_tweet,rel_date_tweet,hap_date_tweet=[],[],[],[]
    flag = 0
    for _ in range(4):
        emotion_dates.append(emotion_filters_date.day)
        date_tweet = get_tweets.filter(date=emotion_filters_date)
        #neg_date_tweet = date_tweet.filter(Q(negative=True)).count()
        sad_date_tweet.append(date_tweet.filter(Q(sad=True)).count())
        anx_date_tweet.append(date_tweet.filter(Q(anxious=True)).count())
        #neu_date_tweet = date_tweet.filter(Q(neutral=True)).count()
        rel_date_tweet.append(date_tweet.filter(Q(relief=True)).count())
        hap_date_tweet.append(date_tweet.filter(Q(happy=True)).count())
        #pos_date_tweet = date_tweet.filter(Q(positive=True)).count()
        if(flag==0):
            max_c = max(sad_date_tweet[0],anx_date_tweet[0],rel_date_tweet[0],hap_date_tweet[0])
            if(max_c==sad_date_tweet[0]):
                max_color = "red"
            if(max_c==anx_date_tweet[0]):
                max_color = "magenta"
            if(max_c==rel_date_tweet[0]):
                max_color = "yellow"
            if(max_c==hap_date_tweet[0]):
                max_color = "green"
        emotion_filters_date -= timedelta(days=1)
        # print(emotion_days[i])
    emotion = {'dates':emotion_dates[::-1],'sad':sad_date_tweet[::-1],'anxious':anx_date_tweet[::-1],'relief':rel_date_tweet[::-1],'happy':hap_date_tweet[::-1]}
    #print(emotion)

    end = time.time()
	
    context = {
        'bar' : True,
        'wordcloud' :settings.MEDIA_ROOT+"/word.png",
        'date': filters_date,
        'loc': filters_loc,
        'content': filters_content,
        'top_5': top_5,
        'pos_neg': pos_neg,
        'emotion': emotion,
        'max_color': max_color,
    }
    #return HttpResponse(f"Runtime of the query is {end - start}")
    return render(request, 'twitter/bar.html',context)

def line(request):
    start = time.time()
    get_tweets = Tweets.objects.all()
    filters_date = date.today()
    filters_content = filters_Default['content']
    filters_loc = filters_Default['loc']

    max_color = "blue"
    
    if(request.method == 'POST'):
        if(request.POST['reset']=='false'):
            filters_date = request.POST['date']
            try:
                filters_date = datetime.strptime(filters_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date() 
            except:
                filters_date = datetime.strptime(filters_date, "%B %d, %Y").date()  
            filters_content = request.POST['content']
            filters_loc = request.POST['loc']
            if(filters_content!="None"):
                get_tweets = get_tweets.filter(tweet__contains=filters_content)
            if(filters_loc!="None"):
              get_tweets = get_tweets.filter(geo=filters_loc)


            print(filters_date,type(filters_content),filters_loc)
        elif(request.POST['reset']=='true'):
            filters_date = filters_Default['date']
            filters_content = filters_Default['content']
            filters_loc = filters_Default['loc']
        
    tweet_cloud = ""
    for tweet in get_tweets:
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

    
    top_5_filters_date = filters_date
    top_5 = word_count(tweet_cloud,stopwords)[:5]
    top_5 = [top[0] for top in top_5]
    count_top_5 = []
    top_5_dates = []
    for _ in range(10):
        top_5_dates.append(top_5_filters_date.day)
        top_5_filters_date -= timedelta(days=1)

    for top in top_5:
        top_tweet = []
        top_5_filters_date = filters_date
        for _ in range(10):
            top_tweet.append(get_tweets.filter(Q(tweet__contains=top[0])|Q(date=top_5_filters_date)).count())
            top_5_filters_date -= timedelta(days=1)
        # print(top)
        count_top_5.append(top_tweet[::-1])
    top_5 = {'terms':top_5,'count':count_top_5,"dates":top_5_dates[::-1]}

    #print(top_5)

    #given_date = "Fri Jun 12 2020 18:11:17 GMT+0530 (India Standard Time)"
    #filters_date = datetime.strptime(given_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date()      
    #print(get_tweets.filter(date=filters_date))

    pos_neg_filters_date = filters_date
    pos_neg_dates = []
    neg_perc = []
    pos_perc = []
    for _ in range(14):
        pos_neg_dates.append(pos_neg_filters_date.day)
        date_tweet = get_tweets.filter(date=pos_neg_filters_date)
        neg_date_tweet = date_tweet.filter(Q(negative=True)|Q(sad=True)|Q(anxious=True)).count()
        pos_date_tweet = date_tweet.filter(Q(positive=True)|Q(happy=True)|Q(relief=True)).count()
        try:
            neg_perc.append(neg_date_tweet/(neg_date_tweet+pos_date_tweet))
            pos_perc.append(pos_date_tweet/(neg_date_tweet+pos_date_tweet))
        except:
            neg_perc.append(0)
            pos_perc.append(0)
        pos_neg_filters_date -= timedelta(days=1)
        # print(pos_neg_days[i])
    pos_neg = {'dates':pos_neg_dates[::-1],'positive':pos_perc[::-1],'negative':neg_perc[::-1]}
    #print(pos_neg)

    emotion_filters_date = filters_date
    emotion_dates = []
    sad_date_tweet,anx_date_tweet,rel_date_tweet,hap_date_tweet=[],[],[],[]
    flag = 0
    for _ in range(8):
        emotion_dates.append(emotion_filters_date.day)
        date_tweet = get_tweets.filter(date=emotion_filters_date)
        #neg_date_tweet = date_tweet.filter(Q(negative=True)).count()
        sad_date_tweet.append(date_tweet.filter(Q(sad=True)).count())
        anx_date_tweet.append(date_tweet.filter(Q(anxious=True)).count())
        #neu_date_tweet = date_tweet.filter(Q(neutral=True)).count()
        rel_date_tweet.append(date_tweet.filter(Q(relief=True)).count())
        hap_date_tweet.append(date_tweet.filter(Q(happy=True)).count())
        #pos_date_tweet = date_tweet.filter(Q(positive=True)).count()
        if(flag==0):
            max_c = max(sad_date_tweet[0],anx_date_tweet[0],rel_date_tweet[0],hap_date_tweet[0])
            if(max_c==sad_date_tweet[0]):
                max_color = "red"
            if(max_c==anx_date_tweet[0]):
                max_color = "magenta"
            if(max_c==rel_date_tweet[0]):
                max_color = "yellow"
            if(max_c==hap_date_tweet[0]):
                max_color = "green"
        emotion_filters_date -= timedelta(days=1)
        # print(emotion_days[i])
    emotion = {'dates':emotion_dates[::-1],'sad':sad_date_tweet[::-1],'anxious':anx_date_tweet[::-1],'relief':rel_date_tweet[::-1],'happy':hap_date_tweet[::-1]}
    #print(emotion)

    end = time.time()
	
    context = {
        'line' : True,
        'wordcloud' :settings.MEDIA_ROOT+"/word.png",
        'date': filters_date,
        'loc': filters_loc,
        'content': filters_content,
        'top_5': top_5,
        'pos_neg': pos_neg,
        'emotion': emotion,
        'max_color': max_color,
    }
    #return HttpResponse(f"Runtime of the query is {end - start}")
    return render(request, 'twitter/line.html',context)

def pie(request):
    start = time.time()
    get_tweets = Tweets.objects.all()
    
    #filters_date = date.today()
    filters_date = datetime.strptime("July 14, 2020", "%B %d, %Y").date() 
    filters_content = filters_Default['content']
    filters_loc = filters_Default['loc']

    max_color = "blue"
    
    if(request.method == 'POST'):
        if(request.POST['reset']=='false'):
            filters_date = request.POST['date']
            try:
                filters_date = datetime.strptime(filters_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date() 
            except:
                filters_date = datetime.strptime(filters_date, "%B %d, %Y").date() 
            filters_content = request.POST['content']
            filters_loc = request.POST['loc']
            if(filters_content!="None"):
                get_tweets = get_tweets.filter(tweet__contains=filters_content)
            if(filters_loc!="None"):
               get_tweets = get_tweets.filter(geo=filters_loc)


            
        elif(request.POST['reset']=='true'):
            filters_date = filters_Default['date']
            filters_content = filters_Default['content']
            filters_loc = filters_Default['loc']
    print(filters_date,type(filters_content),filters_loc)    
    tweet_cloud = ""
    for tweet in get_tweets:
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
    top_5 = [top[0] for top in top_5]
    count_top_5=[]
    for top in top_5:
        count_top_5.append(get_tweets.filter(tweet__contains=top[0]).count())
    top_5 = {'terms':top_5,'count':count_top_5}

    #print(top_5)

    #given_date = "Fri Jun 12 2020 18:11:17 GMT+0530 (India Standard Time)"
    #filters_date = datetime.strptime(given_date[:33], "%a %b %d %Y %H:%M:%S %Z%z").date()      
    #print(get_tweets.filter(date=filters_date))

    emotion_filters_date = filters_date
    sad_date_tweet,anx_date_tweet,rel_date_tweet,hap_date_tweet,pos_date_tweet,neg_date_tweet=0,0,0,0,0,0
    date_tweet = get_tweets.filter(date=emotion_filters_date)
    neg_date_tweet = date_tweet.filter(Q(negative=True)).count()
    sad_date_tweet = date_tweet.filter(Q(sad=True)).count()
    anx_date_tweet = date_tweet.filter(Q(anxious=True)).count()
    #neu_date_tweet = date_tweet.filter(Q(neutral=True)).count()
    rel_date_tweet = date_tweet.filter(Q(relief=True)).count()
    hap_date_tweet = date_tweet.filter(Q(happy=True)).count()
    pos_date_tweet = date_tweet.filter(Q(positive=True)).count()
    max_c = max(sad_date_tweet,anx_date_tweet,rel_date_tweet,hap_date_tweet)
    if(max_c==sad_date_tweet):
        max_color = "red"
    if(max_c==anx_date_tweet):
        max_color = "magenta"
    if(max_c==rel_date_tweet):
        max_color = "yellow"
    if(max_c==hap_date_tweet):
        max_color = "green"
    emotion = {'sad':sad_date_tweet,'anxious':anx_date_tweet,'relief':rel_date_tweet,'happy':hap_date_tweet,'positive':pos_date_tweet,'negative':neg_date_tweet}
    #print(emotion)

    end = time.time()
	
    context = {
        'pie' : True,
        'wordcloud' :settings.MEDIA_ROOT+"/word.png",
        'date': filters_date,
        'loc': filters_loc,
        'content': filters_content,
        'top_5': top_5, 
        'emotion': emotion,
        'max_color': max_color,
    }
    #return HttpResponse(f"Runtime of the query is {end - start}")
    return render(request, 'twitter/pie.html',context)

def deleteTweets(request):
    # batch = Tweets.objects.last().batch
    # Tweets.objects.filter(batch=batch).delete()
    return HttpResponse("This script is commented in order to avoid accidental deletes")

def populateTweets(request):
    batch = 1
    if(Tweets.objects.last()):
        batch = Tweets.objects.last().batch+1
    # print(batch)
    csvFile = 'twitter/tweets_0.csv'
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
                pass
                # print(e)
                # log Error
    
    numberOfTweetsLoaded = Tweets.objects.filter(batch=batch).count()

    return HttpResponse("Batch Number : "+str(batch)+". <br><br>Number of Tweets added successfully :  "+str(numberOfTweetsLoaded)+"/"+str(numberOfRows)+". <br><br>CSV File fetched : '"+str(csvFile.name)+"'")
