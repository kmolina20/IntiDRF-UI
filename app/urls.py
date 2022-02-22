"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from distutils.log import Log
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.views import logout_then_login, LoginView
from django.contrib.auth.decorators import login_required

from usuario.views import Login,LogoutUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inti/', include(('IntiApp.urls','inti'))),
    path('inti/', include('IntiApp.routers')),
    #PERSONALIZED POST QUERIES (only for the view in the API, the links are on the urls.py)
    #path('inti/request/', include('IntiApp.routersCustomRequests')),
    #path('accounts/login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('accounts/login/', Login.as_view(), name="login"),
    path('logout/', login_required(LogoutUser), name="logout"),
   
]

