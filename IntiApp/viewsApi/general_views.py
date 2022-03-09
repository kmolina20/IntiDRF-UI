import json
import requests
import pandas as pd
from traceback import print_tb
from django.http.response import HttpResponse
import services
import requests

from django.shortcuts import redirect, render
from rest_framework import generics


from IntiApp.models import Activity, Company
from IntiApp.serializersApi import general_serializer
from IntiApp.api import GeneralListApiView
from IntiApp.services import *


from time import time
def count_elapsed_time(f):
    """
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """
    def wrapper():
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f()
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        print("Elapsed time: %0.10f seconds." % elapsed_time)
        return ret
    
    return wrapper

@count_elapsed_time
def get_activities():
    url = 'http://localhost:8000/inti/activities' 
    #params = {'year': year, 'author': author}
    r = requests.get(url)
    activities = r.json()
    #print(activities)
    print(activities['next'])
    while (activities['next'] is not None):
        print(activities['next'])
        r = requests.get(activities['next'])
        activities = r.json()
    activities_list = {'activities':activities['results']}
    return activities_list


class ActivityListAPIView(generics.ListAPIView):
    serializer_class = general_serializer.ActivitySerializer

    def get_queryset(self):
        return Activity.objects.all()

class CompanyListAPIView(generics.ListAPIView):
    serializer_class = general_serializer.CompanySerializer

    def get_queryset(self):
        return Company.objects.all()

def index(request):

    '''
    #activities_list = {}
    if request.is_ajax():
        #activities_list = get_activities()
        activities_list = {'activities':'results'}
        return HttpResponse(json.dumps(activities_list),'application/json')
    else:
        return redirect('index')
    '''
    return render(request,'base.html')

def alike_flows(request):
    context = {
        'versions': get_version_specific_names(),
        'intermediate_exchanges': get_intermediate_exchange_name(),
    }

    return render(request,'alike_flows.html',context)

def activities_version(request):
    context = {
        'versions': get_version_specific_names(),
    }

    return render(request,'activities_version.html',context)

def similar_names_activities(request):
    context = {
        'activities': get_activity_name(),
    }

    return render(request,'similar_names.html',context)

def geographies_activities(request):
    context = {
        'geographies': get_geographies(),
    }

    return render(request,'geographies_activities.html',context)

def flows(request):
    context = {
        'flows': get_flows_activities(),
    }
    return render(request,'flows.html',context)

def intermediate_exchange(request):
    context = {
        'versions': get_version_specific_names(),
        'intermediate_exchanges': get_intermediate_exchange(),
    }

    return render(request,'intermediate_exchange.html',context)

def activities(request):
    context = {
        'versions': get_version_specific_names(),   
        'numbersAct': numberActivitiesVersion(),
    }
    return render(request,'activities.html',context)

def start_page(request):
    return render(request,'start_page.html')

def get_activities_csv(request):

        url = 'http://127.0.0.1:8000/inti/activities' 
        #params = {'year': year, 'author': author}
        r = requests.get(url)
        try :
            activities = r.json()
            #print(activities)
            print(activities['next'])
            while (activities['next'] is not None):
                print(activities['next'])
                r = requests.get(activities['next'])
                activities = r.json()
            activities_list = {'activities':activities['results']}
            info = json.loads(activities_list)
            df=pd.json_normalize(info)
            responseCSVActivities = HttpResponse(content_type = 'text/csv')
            responseCSVActivities['Content-Disposition'] = 'attachment;filename="activites.csv"'

            
            df.to_csv(responseCSVActivities)
            return responseCSVActivities
        except:
            print('Error')
'''       
        url = 'http://localhost:8000/inti/activities' 
        r = requests.get(url)
        activities = r.json()
        while (activities['next'] is not None):
            r = requests.get(activities['next'])
            activities = r.json()
            info = json.loads(activities)
            df=pd.json_normalize(info)
            #df.to_csv("dowload.csv")
            all_csv=pd.concat([all_csv,df])
        responseCSVActivities = HttpResponse(content_type = 'text/csv')
        responseCSVActivities['Content-Disposition'] = 'attachment;filename="activites.csv"'

        
        all_csv.to_csv(responseCSVActivities)
        return responseCSVActivities
'''