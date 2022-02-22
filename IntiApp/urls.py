from collections import namedtuple
from django.conf.urls import url
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth.views import logout_then_login,LoginView
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
#from .viewsApi import login
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from IntiApp.viewsApi import login_view,upload_file_requests, upload_LCA_file,general_views

#from IntiApp.viewsApi import general_views

schema_view = get_schema_view(
   openapi.Info(
      title="Inti API",
      default_version='v1',
      description="Public API documentation to manage metadata from life cycle inventory (LCI) data sets in ecoSpold (Ecoinvent)",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mateo.quizhpi@ucuenca.edu.ec"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns=[
    #GENERAL VIEWS  
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #path('actividades/',general_views.ActivityListAPIView.as_view(), name = 'Actividades'),
    #path('companias/',general_views.CompanyListAPIView.as_view(), name = 'Company'),
    path('api_generate_token',views.obtain_auth_token, name = 'Generate Toke'),
    #path('login/',login.Login.as_view(), name = 'Login'),
    #path('logout/',login.Logout.as_view(), name = 'Logout'),
    #path('refresh-token/',login.UserToken.as_view(), name = 'refresh_token'),
    path('home/',login_required(general_views.index),name='index'),
    path('alike_flows/',login_required(general_views.alike_flows),name='alike_flows'), 
    path('activities_version/',login_required(general_views.activities_version),name='activities_version'), 
    path('similar_names_activities/',login_required(general_views.similar_names_activities),name='similar_names_activities'), 
    path('geographies_activities/',login_required(general_views.geographies_activities),name='geographies_activities'), 
    path('flows/',login_required(general_views.flows),name='flows'), 
    path('intermediate_exchange/',login_required(general_views.intermediate_exchange),name='intermediate_exchange'),
    path('upload/', login_required(upload_LCA_file.upload_files), name = "upload_files"), 
    path('query/', login_required(upload_LCA_file.query_files), name = "query_files"),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/',logout_then_login, name = 'logout'),

     #UPLOAD FILE PETITIONS (only for the client .zip)
    path('request_activityIndex/', upload_file_requests.RequestActivityIndex.as_view(),
         name='activityIndex Petitions'),
    path('request_versionNameIndex/', upload_file_requests.RequestVersionNameIndex.as_view(),
         name='versionNameIndex Petitions'),
    path('request_Persons/', upload_file_requests.RequestPersons.as_view(),
         name='person Petitions'),
    path('request_DataGeneratorAndPublication/', upload_file_requests.RequestDataGeneratorAndPublication.as_view(),
         name='DataGeneratorAndPublication Petitions'),
    path('request_Activity/', upload_file_requests.RequestActivity.as_view(),
         name='activity Petitions'),
    path('request_ActivityPerson/', upload_file_requests.RequestActivityPerson.as_view(),
         name='activityPerson Petitions'),
 
]