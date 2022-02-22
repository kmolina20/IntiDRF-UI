import requests

from IntiApp.models import *

def get_activities():
    url = 'http://localhost:8000/inti/activities' 
    #params = {'year': year, 'author': author}
    r = requests.get(url)
    activities = r.json()
    activities_list = {'activities':activities['results']}
    return activities_list

def get_version_names():
    
    versions = Version.objects.all().values('version')
    return versions

def get_activity_name():

    activities = ActivityName.objects.values('activity_name').distinct()  
    return activities

def get_intermediate_exchange():

    activities = IntermediateExchange.objects.values('id').distinct()  
    return activities

def get_geographies():
    geographies = Geography.objects.values('id','name').distinct()
    return geographies 

def get_flows_activities():
    geographies = Activity.objects.values('id','comment_technology').distinct()
    return geographies 
