import requests

from IntiApp.viewsApi.conection import conexion
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

def get_versions():
    versions = Version.objects.values('id','version').distinct().order_by('id')
    return versions

def numberActivitiesVersion():
    data = {}
    data = []
    cursor1 = conexion.cursor()
    for i in range(1,27):
        select = "SELECT count(id) FROM public.activity where version_id='"+str(i)+"';"
        select2 = "SELECT distinct version FROM version where id='"+str(i)+"';"
        cursor1.execute(select)
        select = cursor1.fetchall()
        cursor1.execute(select2)
        select2 = cursor1.fetchall()
        data.append({
            "version": str(select2[0][0]),
            "count": str(select[0][0])
        })
    return data