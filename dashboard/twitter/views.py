from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from django.views.generic import (View,TemplateView,CreateView, DeleteView, DetailView, 
                                    ListView,UpdateView,FormView)
from django.db import transaction
from django.db.models import Avg, Count, F, Aggregate
from django.conf import settings 

def index(request):
    context = {
        'india_map': settings.MEDIA_ROOT+"/india.svg"
    }
    return render(request, 'twitter/index.html',context)
